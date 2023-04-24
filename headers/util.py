from typing import List


def search_with_no_error(headers: List[str], index_name: str, starting_index: int = 0) -> int:
    try:
        return headers.index(index_name, starting_index)
    except ValueError:
        return -1

def search_with_reasonable_error(headers: List[str], index_name: str, starting_index: int = 0) -> int:
    try:
        return headers.index(index_name, starting_index)
    except ValueError:
        raise Exception(index_name + " not included in headers: " + str(headers, starting_index))

def search_with_fallback(headers: List[str], index_name: str, index_name2: str) -> int:
    try:
        return headers.index(index_name)
    except ValueError:
        try:
            return headers.index(index_name2)
        except ValueError:
            raise Exception(index_name + " and " + index_name2 + " not found in headers: " + str(headers))

def safe_int(possible_int: str) -> int:
    try: 
        return int(possible_int)
    except:
        return 0

def safe_float(possible_float: str) -> float:
    try:
        return float(possible_float)
    except:
        return 0.0