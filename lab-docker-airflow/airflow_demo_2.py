from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.bash import BashOperator
import pendulum

# DAG = tarefa/fluxo
with DAG (

    "airflow_demo_1",
    start_date = pendulum.datetime(2024, 9, 3, tz = "UTC"),
    schedule_internal = "0 0 * * 1",

) as dag:
    
    task_1 = EmptyOperator(

        task_id = "nao_faz_nada"
    )

    task_2 = BashOperator(

        task_id = "exemplo_bash",
        bash_command = "echo teste"

    )

    task_1 >> task_2