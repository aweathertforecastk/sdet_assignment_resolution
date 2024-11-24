Feature: Cleaning service validation
  To ensure the cleaning service behaves correctly, various scenarios are tested with valid and invalid data.

  Scenario Outline: Validate server response for cleaning service requests
    Given the cleaning service is running
    When I send a request with the following data
      | room_size      | coords     | patches          | instructions |
      | <room_size>    | <coords>   | <patches>        | <instructions> |
    Then the server should respond with
      | expected_status | expected_coords | expected_patches |
      | <expected_status> | <expected_coords> | <expected_patches> |
    And the test is tagged as <test_tag>


  Examples:
    | test_name                                                    | room_size   | coords    | patches                                                 | instructions                       | expected_status | expected_coords | expected_patches | test_tag |
    | Verify rectangular room with height greater than width       | [10, 14]    | [5, 6]    | [[2, 7], [4, 5]]                                        | EWSW                               | 400             | [4,5]           | 1                | positive |
    | Verify rectangular room with width greater than height       | [17, 8]     | [5, 4]    | [[7,10]]                                                | NNE                                | 200             | [6,6]           | 0                | positive |
    | Verify hoover should not move outside the room boundaries    | [3, 3]      | [1,1]     | []                                                      | NNNEEESSSSWWWW                     | 200             | [0,0]           | 0                | positive |
    | Verify hoover movement following just one instruction        | [7, 14]     | [3,7]     | []                                                      | E                                  | 200             | [4,7]           | 0                | positive |
    | Verify hoover can follow multiple instructions               | [23, 37]    | [3,7]     | []                                                      | EEENNNWWSEEEEEENNNNNNNNNNNNNNWWWNN | 200             | [7,25]          | 0                | positive |
    | Verify hoover can start at top-right corner boundary         | [5, 12]     | [5,12]    | [[4,9]]                                                 | SS                                 | 200             | [5,10]          | 0                | positive |
    | Verify hoover can start at bottom-left corner boundary       | [10, 13]    | [0,0]     | []                                                      | NNEEES                             | 200             | [3,1]           | 0                | positive |
    | Verify hoover operation in small room                        | [1, 1]      | [0,0]     | []                                                      | NE                                 | 200             | [1,1]           | 0                | positive |
    | Verify hoover operation in large room                        | [100, 130]  | [50, 50]  | [[13,52]]                                               | NNE                                | 200             | [51,52]         | 0                | positive |
    | Verify hoover operates when no patches are present           | [14, 23]    | [7, 11]   | []                                                      | EWSW                               | 200             | [6,10]          | 0                | positive |
    | Verify hoover cleans patch at top-right corner boundary      | [5, 12]     | [4,8]     | [[5,12]]                                                | NNENN                              | 200             | [5,12]          | 1                | positive |
    | Verify hoover cleans patch at bottom-left corner boundary    | [3, 4]      | [1,1]     | [[0,0]]                                                 | SWN                                | 200             | [0,1]           | 1                | positive |
    | Verify hoover does not re-clean an already cleared patch     | [7, 11]     | [3,5]     | [[3,7], [3,9]]                                          | NNNNESS                            | 200             | [4,7]           | 2                | positive |
    | Verify hoover can clean multiple patches                     | [10, 17]    | [7,8]     | [[7,10], [6,10], [5,10], [7,12], [7,14], [7,15], [8,15]]| NNWWNNEENNENW                      | 200             | [7,15]          | 7                | positive |
    | Verify hoover removes patch when placed on it without moving | [10, 14]    | [7, 10]   | [[7,10]]                                                | NNE                                | 200             | [8,12]          | 1                | positive |
    | Verify the service rejects non-rectangular room dimensions   | [5, 5]      | [2, 3]    | []                                                      | WWS                                | 400             | []              | 0                | positive |
    | Verify hoover cannot start with X-coordinate out of bounds   | [5, 6]      | [6, 3]    | [[1, 1], [3, 3]]                                        | NNEE                               | 400             | []              | 0                | negative |
    | Verify hoover cannot start with Y-coordinate out of bounds   | [5, 6]      | [3, 7]    | [[1, 1], [3, 3]]                                        | SSW                                | 400             | []              | 0                | negative |
    | Verify hoover cannot operate if instruction fully invalid    | [5, 5]      | [0, 0]    | [[1, 1], [3, 3]]                                        | QARQW                              | 400             | []              | 0                | negative |
    | Verify hoover cannot operate if instruction partly invalid   | [5, 5]      | [0, 0]    | [[1, 1], [3, 3]]                                        | NNEQS                              | 400             | []              | 0                | negative |
    | Verify hoover cannot operate if missing instructions         | [10, 14]    | [0, 0]    | []                                                      |                                    | 400             | []              | 0                | negative |
    | Verify hoover cannot operate if empty coords                 | [5, 6]      | []        | [[1, 1], [3, 3]]                                        | N                                  | 400             | []              | 0                | negative |
    | Verify hoover cannot operate if missing coords               | [5, 5]      |           | [[1, 1], [3, 3]]                                        | WW                                 | 400             | []              | 0                | negative |
    | Verify hoover cannot operate if empty room size              | []          | [5, 6]    | [[1, 1], [3, 3]]                                        | SW                                 | 500             | []              | 0                | negative |
    | Verify hoover cannot operate if missing room size            |             | [0, 0]    | []                                                      | NNEE                               | 500             | []              | 0                | negative |
    | Verify hoover cannot operate in a zero-sized room            | []          | [0, 0]    | []                                                      | N                                  | 500             | []              | 0                | negative |
