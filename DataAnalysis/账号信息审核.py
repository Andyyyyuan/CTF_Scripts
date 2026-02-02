import pandas as pd
import re
from datetime import datetime, date

# ======================================================
# 核心信息合法性验证函数（主流程中调用）
# ======================================================

def check_name(name):
    """姓名：2~4个中文字符"""
    if not isinstance(name, str):
        return False
    return bool(re.fullmatch(r'^[\u4e00-\u9fa5]{2,4}$', name))

def check_phone(phone):
    """手机号：11位数字，以1开头，第二位3-9"""
    if not isinstance(phone, str):
        return False
    return bool(re.fullmatch(r'^1[3-9]\d{9}$', phone))

def check_sfz(sfz):
    """身份证号：18位，最后一位可为X/x，并通过校验码"""
    if not isinstance(sfz, str) or not re.fullmatch(r'^\d{17}[\dXx]$', sfz):
        return False
    weights = [7,9,10,5,8,4,2,1,6,3,7,9,10,5,8,4,2]
    checkcodes = ['1','0','X','9','8','7','6','5','4','3','2']
    total = sum(int(sfz[i]) * weights[i] for i in range(17))
    return checkcodes[total % 11] == sfz[-1].upper()

def check_bankcard(card):
    """银行卡号：16~19位，Luhn算法验证"""
    if not isinstance(card, str) or not re.fullmatch(r'^\d{16,19}$', card):
        return False
    digits = [int(x) for x in card[::-1]]
    s = 0
    for i, d in enumerate(digits):
        if i % 2 == 1:
            d *= 2
            if d > 9:
                d -= 9
        s += d
    return s % 10 == 0

def check_register_date(date_str, sfz):
    """注册日期：格式合法，范围合法，晚于出生日期"""
    try:
        reg_date = datetime.strptime(date_str, "%Y/%m/%d").date()
    except:
        return False

    if not (date(2015,1,1) <= reg_date <= date(2025,10,31)):
        return False

    # 检查身份证出生日期
    try:
        birth_str = sfz[6:14]
        birth_date = datetime.strptime(birth_str, "%Y%m%d").date()
        if reg_date < birth_date:
            return False
    except:
        pass

    return True


# ======================================================
# 扩展验证函数（未在主函数调用，可备用）
# ======================================================

def check_email(email):
    """邮箱格式验证"""
    if not isinstance(email, str):
        return False
    return bool(re.fullmatch(r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$', email))

def check_age_from_sfz(sfz, min_age=18, max_age=100):
    """根据身份证计算年龄并验证是否在范围内"""
    try:
        birth = datetime.strptime(sfz[6:14], "%Y%m%d").date()
        today = date.today()
        age = today.year - birth.year - ((today.month, today.day) < (birth.month, birth.day))
        return min_age <= age <= max_age
    except:
        return False

def check_role(role):
    """角色名称验证（只能包含中英文和下划线，长度2-20）"""
    if not isinstance(role, str):
        return False
    return bool(re.fullmatch(r'^[A-Za-z\u4e00-\u9fa5_]{2,20}$', role))

def check_password_strength(password):
    """密码复杂度：>=8位，含大小写、数字、特殊字符"""
    if not isinstance(password, str) or len(password) < 8:
        return False
    has_upper = re.search(r'[A-Z]', password)
    has_lower = re.search(r'[a-z]', password)
    has_digit = re.search(r'\d', password)
    has_special = re.search(r'[^A-Za-z0-9]', password)
    return all([has_upper, has_lower, has_digit, has_special])


# ======================================================
# 主程序入口
# ======================================================

if __name__ == "__main__":
    input_file = "data.csv"
    output_file = "output.csv"

    df = pd.read_csv(input_file)
    violations = []

    for _, row in df.iterrows():
        issues = []

        if not check_name(row["姓名"]): issues.append("姓名不合法")
        if not check_phone(str(row["手机号"])): issues.append("手机号不合法")
        if not check_sfz(str(row["身份证号"])): issues.append("身份证号不合法")
        if not check_bankcard(str(row["银行卡号"])): issues.append("银行卡号不合法")
        if not check_register_date(str(row["注册日期"]), str(row["身份证号"])): issues.append("注册日期不合法")

        if issues:
            violations.append({
                "姓名": row["姓名"],
                "违规类型": "信息违规",
                "说明": "，".join(issues)
            })

    df_invalid = pd.DataFrame(violations).drop_duplicates(subset=["姓名"])
    df_invalid.to_csv(output_file, index=False, encoding="utf-8-sig")

    print(f"✅ 信息合法性验证完成，违规结果已保存为 UTF-8 编码 CSV：{output_file}")
