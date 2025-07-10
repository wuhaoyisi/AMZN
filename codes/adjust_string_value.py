"""
String Currency Adjustment
Given a string containing both text and numeric values, reduce all numeric values by 15%, and replace them with the updated values in their original positions.
"""
import re

def adjust_string_values(s):
    """
    基础版本：减少字符串中所有数字15%
    处理整数和小数，保持原格式
    """
    def replace_match(match):
        num = float(match.group())
        adjusted = num * 0.85  # 15% reduction
        return f"{adjusted:.2f}"  # Format to 2 decimal places
    
    # 匹配整数和小数
    return re.sub(r"\d+\.?\d*", replace_match, s)

def adjust_string_values_enhanced(s, reduction_percent=15):
    """
    增强版本：支持更多数字格式和自定义减少比例
    支持：负数、货币符号、千分位逗号
    """
    reduction_factor = 1 - (reduction_percent / 100)
    
    def replace_match(match):
        number_str = match.group()
        
        # 提取前缀（符号）和后缀
        prefix = ""
        suffix = ""
        
        # 处理货币符号
        currency_match = re.match(r'^([\$€£¥])', number_str)
        if currency_match:
            prefix = currency_match.group(1)
            number_str = number_str[1:]
        
        # 处理负号
        if number_str.startswith('-'):
            prefix = "-" + prefix
            number_str = number_str[1:]
        
        # 移除千分位逗号
        clean_number = number_str.replace(',', '')
        
        try:
            num = float(clean_number)
            adjusted = num * reduction_factor
            
            # 判断原数字是否为整数
            if '.' not in clean_number:
                # 原数字是整数，保持整数格式
                result = str(int(round(adjusted)))
            else:
                # 原数字是小数，保持两位小数
                result = f"{adjusted:.2f}"
            
            # 重新添加千分位逗号（如果原数字有的话）
            if ',' in number_str and len(result.split('.')[0]) > 3:
                integer_part = result.split('.')[0]
                decimal_part = result.split('.')[1] if '.' in result else ""
                formatted_integer = f"{int(integer_part):,}"
                result = formatted_integer + (f".{decimal_part}" if decimal_part else "")
            
            return prefix + result
            
        except ValueError:
            return match.group()  # 如果转换失败，返回原字符串
    
    # 匹配各种数字格式
    pattern = r'[\$€£¥]?-?\d{1,3}(?:,\d{3})*(?:\.\d+)?'
    return re.sub(pattern, replace_match, s)