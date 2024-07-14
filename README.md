# demo_gcp_llm


Client:
- client/app.py

Server:
- server/use_case_0_intention_detection.py
- server/use_case_1_resource_exploration.py
- server/use_case_2_query_generation.py

Server Testing:
- server/example_request/use_case_0.py
- server/example_request/use_case_1.py
- server/example_request/use_case_2.py

Data:
- data/resource_catalog.txt
- data/data_catalog.txt


Example User Input (Prompt):

use-case 0:
- How many user are assgined to each doctor in the hospital
- Is there any data about Emergency cases
- Spaghetti is Yummy!

use-case 1:
- Is there any information about schedule of the staff
- Is there any data about Emergency cases
- Is there any report about Pokemon

use-case 2:
- Is there any repeated patient in 1 month
- Generate the SQL query for analyzing patient distribution among the wards
- How many user are assgined to each doctor in the hospital



Run Server
```
gcloud auth application-default login
python3 run ./server/use_case_[NAME].py
```

Run Client
```
streamlit run ./client/app.py
```