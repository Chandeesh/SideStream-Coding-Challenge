"""Module to setup fastapi API to expose API to the outside world."""
import logging
from loguru import logger
import random
from typing import Any, Dict
from typing import Optional
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import sys
from pydantic import BaseModel

class Item(BaseModel):
    resolvedCount: list

req_count = 0
operators = {}

ERROR_CODES = [error_code for error_code in range(50)]
app = FastAPI()

origins = [
    "http://localhost:8080",
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#logging to out.log file
logger.add(sys.stderr, format="{time} {level} {message}", level="INFO")
logger.add("out.log", backtrace=True, diagnose=True)

def _generate_lists() -> Dict[str, Any]:
    """Generate resolved, unresolved and backlog lists."""
    return {
        'resolved': [{
            'index': error_idx,
            'code': random.choice(ERROR_CODES),
            'text': 'Error ABC occured, that is `resolved`'
        } for error_idx in range(50)],
        'unresolved': [{
            'index': error_idx,
            'code': random.choice(ERROR_CODES),
            'text': 'Error DEF occured, that is `unresolved`'
        } for error_idx in range(50, 100)],
        'backlog': [{
            'index': error_idx,
            'code': random.choice(ERROR_CODES),
            'text': 'Error XYZ occured, that is in the `backlog`'
        } for error_idx in range(100, 150)]
    }

#function to store request count for the operator
def _log_requests(name):
    global operators
    global req_count
    if(len(operators)==0):
        operators[name] = req_count
    elif name not in operators:
        operators[name] = req_count
    return operators

def _update_log_requests(operators,name):
    operators[name] = operators[name]+1
    return operators

#function to find the intersection count
def find_intersect(res,unres):
    count = 0
    for x in range(1,len(res)):
        for y in range(1,len(unres)):
            if res[x]['code']==unres[y]['code']:
                count = count + 1
    return count

#end point to calculate resolved count
@app.post("/resolvedcount")
def create_item(item: Item):
    for x in item.resolvedCount:
        logger.info("Code: "+str(x['code'])+" Count: "+str(x['count']))
        print("Code: "+str(x['code'])+" Count: "+str(x['count']))
    return item

@app.get("/get_lists")
def get_lists(operator_name: Optional[str] = "") -> Dict[str, Any]:
    """Return resolved, unresolved and backlog lists."""
    operators = _log_requests(operator_name)
    operators = _update_log_requests(operators,operator_name)
    logger.info("Operator_Name: " +operator_name + " Request_Count: " + str(operators[operator_name]))
    return _generate_lists()


@app.get("/get_list_intersection_counts")
def get_list_intersection_counts() -> Dict[str, int]:
    
    logger.info('Generating the intersection counts between a set of resolved, unresolved and backlog lists.')

    error_lists = _generate_lists()
    resolved, unresolved, backlog = error_lists['resolved'], error_lists['unresolved'], error_lists['backlog']
    
    return {
        'resolved_unresolved' : find_intersect(resolved,unresolved),
        'resolved_backklog' : find_intersect(resolved,backlog),
        'unresolved_backlog' : find_intersect(unresolved,backlog)
    }
    # NOTE: THIS IS JUST AN EXAMPLE, REPLACE WITH YOUR OWN CODE AND `return`!


def run(host: str, port: int) -> None:
    """Run the code challenge API."""
    uvicorn.run(app, host=host, port=port)