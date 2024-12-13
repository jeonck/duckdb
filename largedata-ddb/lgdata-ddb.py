import pandas as pd
import numpy as np
import duckdb
import time

# 대용량 데이터 생성 함수
def generate_large_data(rows=10_000_000, columns=10):
    """
    rows: 생성할 데이터의 행 수
    columns: 생성할 데이터의 열 수
    """
    data = {
        f"col_{i}": np.random.randint(0, 100, size=rows) for i in range(columns)
    }
    data["category"] = np.random.choice(["A", "B", "C", "D"], size=rows)
    return pd.DataFrame(data)

# DuckDB를 활용한 병렬 처리 테스트
def test_duckdb_parallel(dataframe):
    """
    dataframe: 처리할 Pandas DataFrame
    """
    conn = duckdb.connect(":memory:")  # 메모리 내에서 DuckDB 실행
    conn.execute("PRAGMA threads=4")  # 병렬 처리 스레드 수 설정 (4개 스레드)

    print("Loading data into DuckDB...")
    conn.register("large_table", dataframe)  # 데이터프레임을 DuckDB에 등록

    print("Running aggregation query...")
    start_time = time.time()
    result = conn.execute("""
        SELECT 
            category, 
            AVG(col_1) AS avg_col_1, 
            SUM(col_2) AS sum_col_2, 
            COUNT(*) AS total_rows 
        FROM large_table 
        GROUP BY category
    """).fetchdf()
    end_time = time.time()

    print("Query executed in {:.2f} seconds.".format(end_time - start_time))
    print("Result:")
    print(result)

if __name__ == "__main__":
    print("Generating large dataset...")
    large_data = generate_large_data(rows=10_000_000, columns=10)  # 1000만 행 데이터 생성

    print("Testing DuckDB parallel processing...")
    test_duckdb_parallel(large_data)
