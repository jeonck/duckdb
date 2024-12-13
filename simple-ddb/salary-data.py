import duckdb
import pandas as pd

def create_sample_data():
    """샘플 데이터 생성 및 CSV 파일로 저장"""
    data = {
        "name": ["Alice", "Bob", "Charlie", "Diana"],
        "age": [25, 30, 35, 40],
        "salary": [50000, 60000, 70000, 80000],
    }
    df = pd.DataFrame(data)
    csv_file = "sample.csv"
    df.to_csv(csv_file, index=False)
    return df, csv_file

def analyze_with_duckdb(csv_file):
    """DuckDB를 사용한 데이터 분석"""
    con = duckdb.connect()
    con.execute(f"CREATE TABLE employees AS SELECT * FROM read_csv_auto('{csv_file}')")
    result = con.execute("""
        SELECT 
            AVG(age) AS avg_age, 
            SUM(salary) AS total_salary 
        FROM employees
    """).fetchall()
    return result[0]

def process_with_pandas(df):
    """Pandas를 사용한 데이터 처리"""
    filtered_df = df[df['age'] >= 30].copy()
    filtered_df['salary'] = filtered_df['salary'] * 1.1
    return filtered_df

def main():
    # 데이터 생성
    df, csv_file = create_sample_data()
    
    # DuckDB 분석
    avg_age, total_salary = analyze_with_duckdb(csv_file)
    print(f"DuckDB - 평균 나이: {avg_age}, 총 급여: {total_salary}")
    
    # Pandas 처리
    result_df = process_with_pandas(df)
    print("\nPandas - 필터링 및 매핑 결과:")
    print(result_df)

if __name__ == "__main__":
    main()
