"""
安全审计脚本
"""
import os
import sys
import ast
import re
from typing import List, Dict, Any

class SecurityAuditor:
    def __init__(self):
        self.issues = []
        
    def check_file(self, filepath: str):
        """检查单个文件的安全问题"""
        with open(filepath, 'r') as f:
            content = f.read()
            
        # 检查源代码
        tree = ast.parse(content)
        
        # 检查AST
        visitor = SecurityVisitor(filepath)
        visitor.visit(tree)
        self.issues.extend(visitor.issues)
        
        # 检查字符串模式
        self._check_patterns(content, filepath)
    
    def _check_patterns(self, content: str, filepath: str):
        """检查常见的安全问题模式"""
        patterns = {
            r"eval\(": "使用eval可能导致代码注入",
            r"exec\(": "使用exec可能导致代码注入",
            r"os\.system\(": "使用os.system可能存在命令注入风险",
            r"subprocess\.": "使用subprocess需要注意命令注入",
            r"input\(": "直接使用input可能存在安全风险",
            r"\.format\(.*\)": "使用字符串format需要注意格式化字符串漏洞",
            r"%[sd]": "使用%格式化需要注意格式化字符串漏洞"
        }
        
        for pattern, message in patterns.items():
            if re.search(pattern, content):
                self.issues.append({
                    'file': filepath,
                    'type': 'pattern_match',
                    'message': message
                })
    
    def audit_directory(self, directory: str):
        """审计整个目录"""
        for root, _, files in os.walk(directory):
            for file in files:
                if file.endswith('.py'):
                    filepath = os.path.join(root, file)
                    self.check_file(filepath)
    
    def generate_report(self) -> str:
        """生成审计报告"""
        if not self.issues:
            return "✅ 未发现安全问题"
        
        report = ["🚨 安全审计报告", "=" * 20, ""]
        
        for issue in self.issues:
            report.append(f"文件: {issue['file']}")
            report.append(f"类型: {issue['type']}")
            report.append(f"问题: {issue['message']}")
            report.append("-" * 20)
        
        return "\n".join(report)

class SecurityVisitor(ast.NodeVisitor):
    def __init__(self, filepath: str):
        self.issues = []
        self.filepath = filepath
    
    def visit_Call(self, node: ast.Call):
        """检查函数调用"""
        if isinstance(node.func, ast.Name):
            if node.func.id in ['eval', 'exec']:
                self.issues.append({
                    'file': self.filepath,
                    'type': 'dangerous_call',
                    'message': f'使用了危险函数: {node.func.id}'
                })
        self.generic_visit(node)
    
    def visit_Import(self, node: ast.Import):
        """检查导入"""
        dangerous_modules = ['pickle', 'marshal']
        for name in node.names:
            if name.name in dangerous_modules:
                self.issues.append({
                    'file': self.filepath,
                    'type': 'dangerous_import',
                    'message': f'导入了不安全的模块: {name.name}'
                })
        self.generic_visit(node)

def main():
    """主函数"""
    if len(sys.argv) != 2:
        print("使用方法: python security_audit.py <目录路径>")
        sys.exit(1)
    
    directory = sys.argv[1]
    if not os.path.exists(directory):
        print(f"错误: 目录不存在: {directory}")
        sys.exit(1)
    
    auditor = SecurityAuditor()
    auditor.audit_directory(directory)
    report = auditor.generate_report()
    print(report)

if __name__ == "__main__":
    main() 