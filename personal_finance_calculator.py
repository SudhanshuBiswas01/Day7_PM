"""
Assignment: Personal Finance Calculator
Parts A, B, C, D — Complete Submission
"""

# =============================================================================
# PART A & B: Personal Finance Calculator with Indian Formatting
# =============================================================================


def format_indian(amount: float) -> str:
    """
    Format a number in Indian lakh/crore style with ₹ symbol.

    Args:
        amount: The numeric value to format.

    Returns:
        A string formatted in Indian currency style (e.g., ₹12,00,000.00).
    """
    
    is_negative = amount < 0
    amount = abs(amount)
    integer_part, decimal_part = f"{amount:.2f}".split(".")

    # Indian grouping: last 3 digits, then groups of 2
    digits = list(integer_part)
    if len(digits) > 3:
        result = "," + ",".join(
            "".join(digits[max(0, i):i + 2])
            for i in range(len(digits) - 3, 0, -2)
            if digits[max(0, i):i + 2]
        )
        # Rebuild properly
        n = integer_part
        last_three = n[-3:]
        rest = n[:-3]
        groups = []
        while rest:
            groups.append(rest[-2:])
            rest = rest[:-2]
        groups.reverse()
        formatted = ",".join(groups) + "," + last_three
    else:
        formatted = integer_part

    prefix = "-₹" if is_negative else "₹"
    return f"{prefix}{formatted}.{decimal_part}"


def get_float_input(prompt: str, min_val: float, max_val: float) -> float:
    """
    Prompt user for a float input with validation.

    Args:
        prompt: The message shown to the user.
        min_val: Minimum acceptable value (exclusive for 0-checks).
        max_val: Maximum acceptable value.

    Returns:
        A validated float value from user input.
    """
    while True:
        try:
            value = float(input(prompt))
            if value < min_val or value > max_val:
                print(f"  ⚠ Value must be between {min_val} and {max_val}. Try again.")
            else:
                return value
        except ValueError:
            print("  ⚠ Invalid input. Please enter a number.")


def collect_employee_data(label: str = "") -> dict:
    """
    Collect and validate financial data for one employee.

    Args:
        label: Optional label like 'Employee 1' for multi-employee mode.

    Returns:
        A dictionary with validated employee financial data.
    """
    tag = f"[{label}] " if label else ""
    print(f"\n  {'─' * 40}")
    print(f"  Enter details for {label if label else 'Employee'}:")
    print(f"  {'─' * 40}")

    name = input(f"  {tag}Employee Name       : ").strip()
    while not name:
        print("  ⚠ Name cannot be empty.")
        name = input(f"  {tag}Employee Name       : ").strip()

    annual_salary = get_float_input(
        f"  {tag}Annual Salary (₹)   : ", 0.01, float("inf")
    )
    tax_percentage = get_float_input(
        f"  {tag}Tax Bracket (0–50%) : ", 0.0, 50.0
    )
    monthly_rent = get_float_input(
        f"  {tag}Monthly Rent (₹)    : ", 0.01, float("inf")
    )
    savings_percentage = get_float_input(
        f"  {tag}Savings Goal (0–100%): ", 0.0, 100.0
    )

    return {
        "name": name,
        "annual_salary": annual_salary,
        "tax_percentage": tax_percentage,
        "monthly_rent": monthly_rent,
        "savings_percentage": savings_percentage,
    }


def calculate_finances(data: dict) -> dict:
    """
    Perform all financial calculations for a single employee.

    Args:
        data: Dictionary containing employee financial inputs.

    Returns:
        A dictionary with all computed financial values.
    """
    monthly_salary = data["annual_salary"] / 12
    monthly_tax = monthly_salary * (data["tax_percentage"] / 100)
    net_salary = monthly_salary - monthly_tax
    rent_ratio = (data["monthly_rent"] / net_salary) * 100 if net_salary > 0 else 0
    monthly_savings = net_salary * (data["savings_percentage"] / 100)
    disposable_income = net_salary - data["monthly_rent"] - monthly_savings

    return {
        "monthly_salary": monthly_salary,
        "monthly_tax": monthly_tax,
        "net_salary": net_salary,
        "rent_ratio": rent_ratio,
        "monthly_savings": monthly_savings,
        "disposable_income": disposable_income,
        "annual_tax": monthly_tax * 12,
        "annual_savings": monthly_savings * 12,
        "annual_rent": data["monthly_rent"] * 12,
    }


def print_financial_report(data: dict, calc: dict) -> None:
    """
    Print a formatted financial summary report for one employee.

    Args:
        data: Employee input data dictionary.
        calc: Calculated financial values dictionary.
    """
    w = 44
    print(f"\n{'═' * w}")
    print(f"{'EMPLOYEE FINANCIAL SUMMARY':^{w}}")
    print(f"{'═' * w}")
    print(f" Employee      : {data['name']}")
    print(f" Annual Salary : {format_indian(data['annual_salary'])}")
    print(f"{'─' * w}")
    print(" Monthly Breakdown:")
    print(f"   Gross Salary     : {format_indian(calc['monthly_salary']):>16}")
    print(f"   Tax ({data['tax_percentage']:.1f}%)      : {format_indian(calc['monthly_tax']):>16}")
    print(f"   Net Salary       : {format_indian(calc['net_salary']):>16}")
    print(f"   Rent             : {format_indian(data['monthly_rent']):>16}  ({calc['rent_ratio']:.1f}% of net)")
    print(f"   Savings ({data['savings_percentage']:.1f}%)  : {format_indian(calc['monthly_savings']):>16}")
    print(f"   Disposable       : {format_indian(calc['disposable_income']):>16}")
    print(f"{'─' * w}")
    print(" Annual Projection:")
    print(f"   Total Tax        : {format_indian(calc['annual_tax']):>16}")
    print(f"   Total Savings    : {format_indian(calc['annual_savings']):>16}")
    print(f"   Total Rent       : {format_indian(calc['annual_rent']):>16}")
    print(f"{'═' * w}")


def financial_health_score(data: dict, calc: dict) -> int:
    """
    Calculate a financial health score from 0 to 100.

    Scoring formula (justified):
      - Rent Ratio Score  (40 pts): <30% = 40, <40% = 25, <50% = 10, else = 0
        Rationale: Housing > 50% of net income is financially dangerous.
      - Savings Score     (40 pts): proportional to savings_percentage / 30 * 40
        Rationale: 30% savings rate is considered excellent; scored linearly.
      - Disposable Score  (20 pts): disposable / net * 20
        Rationale: Having leftover income after rent + savings = buffer for life.

    Args:
        data: Employee input dictionary.
        calc: Computed financial values.

    Returns:
        An integer score between 0 and 100.
    """
    # Rent score
    rent_ratio = calc["rent_ratio"]
    if rent_ratio < 30:
        rent_score = 40
    elif rent_ratio < 40:
        rent_score = 25
    elif rent_ratio < 50:
        rent_score = 10
    else:
        rent_score = 0

    # Savings score (max at 30% savings rate)
    savings_score = min(40, (data["savings_percentage"] / 30) * 40)

    # Disposable income score
    disposable_ratio = calc["disposable_income"] / calc["net_salary"] if calc["net_salary"] > 0 else 0
    disposable_score = max(0, disposable_ratio * 20)

    return int(rent_score + savings_score + disposable_score)


def print_comparison_table(emp1_data: dict, emp1_calc: dict,
                            emp2_data: dict, emp2_calc: dict) -> None:
    """
    Print a side-by-side comparison table for two employees.

    Args:
        emp1_data: Input data for Employee 1.
        emp1_calc: Calculations for Employee 1.
        emp2_data: Input data for Employee 2.
        emp2_calc: Calculations for Employee 2.
    """
    score1 = financial_health_score(emp1_data, emp1_calc)
    score2 = financial_health_score(emp2_data, emp2_calc)

    col = 20
    sep = "─" * (col + 1)

    print(f"\n{'═' * 62}")
    print(f"{'EMPLOYEE COMPARISON':^62}")
    print(f"{'═' * 62}")
    print(f"  {'Metric':<22} {'Emp 1':>{col}} {'Emp 2':>{col}}")
    print(f"  {'─' * 22} {sep} {sep}")

    rows = [
        ("Name",            emp1_data["name"],                             emp2_data["name"]),
        ("Annual Salary",   format_indian(emp1_data["annual_salary"]),     format_indian(emp2_data["annual_salary"])),
        ("Monthly Net",     format_indian(emp1_calc["net_salary"]),        format_indian(emp2_calc["net_salary"])),
        ("Tax %",           f"{emp1_data['tax_percentage']:.1f}%",         f"{emp2_data['tax_percentage']:.1f}%"),
        ("Monthly Tax",     format_indian(emp1_calc["monthly_tax"]),       format_indian(emp2_calc["monthly_tax"])),
        ("Monthly Rent",    format_indian(emp1_data["monthly_rent"]),      format_indian(emp2_data["monthly_rent"])),
        ("Rent Ratio",      f"{emp1_calc['rent_ratio']:.1f}%",             f"{emp2_calc['rent_ratio']:.1f}%"),
        ("Monthly Savings", format_indian(emp1_calc["monthly_savings"]),   format_indian(emp2_calc["monthly_savings"])),
        ("Disposable",      format_indian(emp1_calc["disposable_income"]), format_indian(emp2_calc["disposable_income"])),
        ("Health Score",    f"{score1}/100",                               f"{score2}/100"),
    ]

    for label, v1, v2 in rows:
        print(f"  {label:<22} {v1:>{col}} {v2:>{col}}")

    print(f"{'═' * 62}")

    winner = emp1_data["name"] if score1 >= score2 else emp2_data["name"]
    print(f"\n  🏆 Better financial health: {winner} (Score: {max(score1, score2)}/100)")
    print(f"  Formula: Rent(40pts) + Savings(40pts) + Disposable(20pts)")
    print(f"{'═' * 62}\n")





# =============================================================================
# MAIN — Entry Point
# =============================================================================

def main() -> None:
    """
    Main entry point for the Personal Finance Calculator.

    Runs single employee report (Part A) and two-employee
    comparison with health scoring (Part B).
    """
    print("\n╔══════════════════════════════════════════╗")
    print("║   PERSONAL FINANCE CALCULATOR            ║")
    print("║   AI Startup Employee Benefits Portal    ║")
    print("╚══════════════════════════════════════════╝")

    print("\n  Mode: Two-Employee Comparison (Part B)")

    emp1_data = collect_employee_data("Employee 1")
    emp2_data = collect_employee_data("Employee 2")

    emp1_calc = calculate_finances(emp1_data)
    emp2_calc = calculate_finances(emp2_data)

    # Part A: Individual reports
    print_financial_report(emp1_data, emp1_calc)
    print_financial_report(emp2_data, emp2_calc)

    # Part B: Side-by-side comparison + health scores
    print_comparison_table(emp1_data, emp1_calc, emp2_data, emp2_calc)

    # Part C: Demonstrate analyze_value
    print("\n── Part C: analyze_value() Demo ──────────────")
    print(analyze_value(42))
    print(analyze_value(""))
    print(analyze_value([1, 2, 3]))
    print(analyze_value(True))
    print(analyze_value((1, 2)))
    print("──────────────────────────────────────────────\n")


if __name__ == "__main__":
    main()