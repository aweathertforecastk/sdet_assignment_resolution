Feature: Cleaning service validation
  To ensure the cleaning service behaves correctly, various scenarios are tested with valid and invalid data.
  
  
  @positive
  Scenario Outline: Verify server response for cleaning service requests with valid data
    Given the cleaning service is running
    When I send a request with the following data
      | roomSize      | coords     | patches          | instructions |
      | <roomSize>    | <coords>   | <patches>        | <instructions> |
    Then the server should respond with
      | expected_status | expected_coords | expected_patches |
      | <expected_status> | <expected_coords> | <expected_patches> |


  Examples: Positive tests
    | test_name                                                    | roomSize    | coords    | patches                                                 | instructions                       | expected_status | expected_coords | expected_patches|
    | Verify rectangular room with height greater than width       | [10, 14]    | [5, 6]    | [[2, 7], [4, 5]]                                        | EWSW                               | 200             | [4, 5]          | 1               |
    | Verify rectangular room with width greater than height       | [17, 8]     | [5, 4]    | [[7, 10]]                                               | NNE                                | 200             | [6, 6]          | 0               |
    | Verify hoover should not move outside the room boundaries    | [3, 3]      | [1, 1]    | [1, 2]                                                  | NNNEEESSSSWWWW                     | 200             | [0, 0]          | 1               | 
    | Verify hoover movement following just one instruction        | [7, 14]     | [3, 7]    | [5, 5]                                                  | E                                  | 200             | [4, 7]          | 0               |
    | Verify hoover can follow multiple instructions               | [23, 37]    | [3, 7]    | [0, 1]                                                  | EEENNNWWSEEEEEENNNNNNNNNNNNNNWWWNN | 200             | [7, 25]         | 0               |
    | Verify hoover can start at top-right corner boundary         | [5, 12]     | [5, 12]   | [[4, 9]]                                                | SS                                 | 200             | [5, 10]         | 0               |
    | Verify hoover can start at bottom-left corner boundary       | [10, 13]    | [0, 0]    | [4, 5]                                                  | NNEEES                             | 200             | [3, 1]          | 0               |
    | Verify hoover operation in small room                        | [1, 1]      | [0, 0]    | [1, 0]                                                  | NE                                 | 200             | [1, 1]          | 0               |
    | Verify hoover operation in large room                        | [100, 130]  | [50, 50]  | [13, 52]                                                | NNE                                | 200             | [51, 52]        | 0               | 
    | Verify hoover operates when no patches are present           | [14, 23]    | [7, 11]   | []                                                      | EWSW                               | 200             | [6, 10]         | 0               |
    | Verify hoover cleans patch at top-right corner boundary      | [5, 12]     | [4, 8]    | [[5, 12]]                                               | NNENN                              | 200             | [5, 12]         | 1               |
    | Verify hoover cleans patch at bottom-left corner boundary    | [3, 4]      | [1, 1]    | [[0, 0]]                                                | SWN                                | 200             | [0, 1]          | 1               |
    | Verify hoover does not re-clean an already cleared patch     | [7, 11]     | [3, 5]    | [[3, 7], [3, 9]]                                        | NNNNSSS                            | 200             | [3, 6]          | 2               |
    | Verify hoover can clean multiple patches                     | [10, 17]    | [7, 8]    | [[7, 10], [6,10], [5,10], [7,12], [7,14], [7,15] ]      | NNWWNNEENNENW                      | 200             | [7, 15]         | 6               |
    | Verify hoover removes patch when placed on it without moving | [10, 14]    | [7, 10]   | [[7, 10]]                                               | NNE                                | 200             | [8, 12]         | 1               |
    


  @negative
  Scenario Outline: Verify server response for cleaning service requests with invalid data
    Given the cleaning service is running
    When I send a request with the following data
      | roomSize      | coords     | patches          | instructions |
      | <roomSize>    | <coords>   | <patches>        | <instructions> |
    Then the server should respond with
      | expected_status | expected_coords | expected_patches |
      | <expected_status> | <expected_coords> | <expected_patches> |


  Examples: Negative tests
    | test_name                                                    | roomSize   | coords     | patches                                                 | instructions                       | expected_status | expected_coords | expected_patches |
    | Verify hoover cannot start with X-coordinate out of bounds   | [5, 6]      | [6, 3]    | [[1, 2], [3, 3]]                                        | NNEE                               | 400             | []              | 0                |
    | Verify hoover cannot start with Y-coordinate out of bounds   | [5, 6]      | [3, 7]    | [[1, 5], [3, 2]]                                        | SSW                                | 400             | []              | 0                |
    | Verify hoover cannot operate if instruction fully invalid    | [5, 5]      | [0, 0]    | [[1, 1], [3, 4]]                                        | QARQM                              | 400             | []              | 0                |
    | Verify hoover cannot operate if instruction partly invalid   | [5, 5]      | [0, 0]    | [[1, 1], [1, 1]]                                        | NNEQS                              | 400             | []              | 0                |
    | Verify hoover cannot operate if missing instructions         | [10, 14]    | [0, 0]    | []                                                      |                                    | 400             | []              | 0                |
    | Verify hoover cannot operate if empty coords                 | [5, 6]      | []        | [[1, 1], [3, 3]]                                        | N                                  | 400             | []              | 0                |
    | Verify hoover cannot operate if missing coords               | [5, 5]      |           | [[1, 1], [0, 3]]                                        | WW                                 | 400             | []              | 0                |
    | Verify hoover cannot operate if empty room size              | []          | [5, 6]    | [[1, 1], [3, 1]]                                        | SW                                 | 400             | []              | 0                |
    | Verify hoover cannot operate if missing room size            |             | [0, 0]    | []                                                      | NNEE                               | 400             | []              | 0                |
    | Verify hoover cannot operate in a zero-sized room            | [0, 0]      | [0, 0]    | []                                                      | N                                  | 400             | []              | 0                |
    | Verify inappropriate character (letter) in room_size X       | ["A", 12]   | [5, 12]   | [[4,9]]                                                 | SS                                 | 400             | []              | 0                |
    | Verify inappropriate character (letter) in room_size Y       | [10, "b"]   | [0, 0]    | []                                                      | NNEEES                             | 400             | []              | 0                |
    | Verify inappropriate character (letter) in coords X          | [2, 1]      | ["C", 0]  | []                                                      | NE                                 | 400             | []              | 0                |
    | Verify inappropriate character (letter) in coords Y          | [100, "S"]  | [50, "n"] | [[13, 52]]                                              | NNE                                | 400             | []              | 0                |
    | Verify inappropriate character (letter) in patches X         | [14, 23]    | [7, 11]   | [["x", 3]]                                              | EWSW                               | 400             | []              | 0                |
    | Verify inappropriate character (letter) in patches Y         | [5, 12]     | [4, 8]    | [[1, "P"]]                                              | NNENN                              | 400             | []              | 0                |
    | Verify inappropriate character (symbol) in room_size X       | ["@", 4]    | [1, 1]    | [[0, 0]]                                                | SWN                                | 400             | []              | 0                |
    | Verify inappropriate character (symbol) in room_size Y       | [7, "#"]    | [3, 5]    | [[3, 7], [3, 9]]                                        | NNNNESS                            | 400             | []              | 0                |
    | Verify inappropriate character (symbol) in coords X          | [10, 17]    | ["!" ,8]  | [ [7, 10], [6, 10], [5, 10], [7, 12], [7, 14], [7, 15] ]| NNWWNNEENNENW                      | 400             | []              | 0                |
    | Verify inappropriate character (symbol) in coords Y          | [10, 14]    | [7, "?"]  | [[7, 3]]                                                | NNE                                | 400             | []              | 0                |
    | Verify inappropriate character (symbol) in patches X         | [5, 5]      | [2, 3]    | [["$", 3]]                                              | WWS                                | 400             | []              | 0                |
    | Verify inappropriate character (symbol) in patches Y         | [5, 6]      | [6, 3]    | [[1, 5], [3, "*"]]                                      | NNEE                               | 400             | []              | 0                |
    | Verify inappropriate character (symbol) in instructions      | [5, 6]      | [3, 7]    | [[1, 1], [3, 3]]                                        | SS"-"W                             | 400             | []              | 0                |
    | Verify invalid input: missing parameter in room_size X       | [ , 12]     | [5, 12]   | [[4,9]]                                                 | SS                                 | 400             | []              | 0                |
    | Verify invalid input: missing parameter in room_size Y       | [10, ]      | [0, 0]    | []                                                      | NNEEES                             | 400             | []              | 0                |
    | Verify invalid input: missing parameter in coords X          | [4, 1]      | [ ,0]     | []                                                      | NE                                 | 400             | []              | 0                |
    | Verify invalid input: missing parameter in coords Y          | [100, 110]  | [50, ]    | [[13, 52]]                                              | EWSW                               | 400             | []              | 0                |
    | Verify invalid input: missing parameter in patches X         | [14, 23]    | [7, 11]   | [[, 3]]                                                 | EWSW                               | 400             | []              | 0                |
    | Verify invalid input: missing parameter in patches Y         | [14, 23]    | [7, 11]   | [[5, ]]                                                 | EWSW                               | 400             | []              | 0                |
    | Verify input validation for integer in instructions          | [14, 23]    | [7, 11]   | [[5, 7]]                                                | EW5SW                              | 400             | []              | 0                |



