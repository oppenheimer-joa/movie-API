
from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.bash import BashOperator
from airflow.operators.empty import EmptyOperator
import pendulum
from airflow.models.variable import Variable

local_tz = pendulum.timezone("Asia/Seoul")

default_args = {
    'owner': 'SMS',
    'depends_on_past': True,
    'start_date': datetime(2023, 2, 1, 0, 0, 0, tzinfo=local_tz),
    'retries': 1,
    "retry_delay": timedelta(minutes=1)
}
dag = DAG(
    dag_id='MOVIES.Details',
    description='영화상세정보 받기',
    default_args=default_args,
    schedule_interval="0 0 * * 0",
    max_active_runs=1,  # 동시에 실행되는 DAG의 수
    concurrency=1,  # 동시에 실행되는 작업의 수
)


HOME_DIR = '/home/kjh/code/SMS/movie-API'
LIST_DIR = '/home/kjh/code/SMS/movie-API/Data/movieDetails'

start = EmptyOperator(
    task_id='start',
    dag=dag
)

get_MovieDetails = BashOperator(
    task_id='get.MOVIE.Details',
    bash_command=f'''
        curl -X POST "http://IP:PORT/flag-endpoint" -H "accept: text/plain" -H "Content-Type: application/json" -d '{"FLAG_DIR":"/home/kjh/code/FastAPI-demo/datas/DONE","check_time":3600,"interval":1}'
        ''',
    retries=3,
    retry_delay=timedelta(seconds=10),
    dag=dag
)

end = BashOperator(
    task_id='end',
    bash_command="echo 'END'",
    dag=dag
)

# Set task dependencies
start >> get_MovieDetails >> end
