
1. pip install -r requirements.txt
2. uvicorn app.main:app --reload
3. copy the port link it provides -> go to postman -> change to POST -> paste link -> add '/predict' as 'link/predict'
4. go to body -> raw -> 
{
  "city_name": "Noida"
}
5. Run :)