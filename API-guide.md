# IN PROGRESS THERE IS NO CODE IN REPO YET OR ONLINE !!!!!!
> IN PROGRESS !!!!!!



| Resource                                              | GET                                                 | POST                                  | PUT                               | DELETE                                      |
| ----------------------------------------------------- | --------------------------------------------------- | ------------------------------------- | --------------------------------- | ------------------------------------------- |
| [/api/v1/](#URIs_list)                             | Returns a list of links to the other available URIs | N/A                                   | N/A                               | N/A                                         |
| [/api/v1/patients/](#Patient_list)                                 | Returns a list of patients                           | Creates a new patient                  | N/A                               | N/A                                         |
| [/readers/{id}](#reader)                             | Returns the details of a single reader              | N/A                                   | Updates a reader                  | Deletes a reader                            |


## Resources
### URIs_list

| URI | Method   |**GET** |
| --- |  ------- |  ------- |
| `/api/v1/`  | Permission |All      |


##### GET

Returns list of avalible URIs.

### Patient_list

| URI                  | Method         |**GET**     |**POST** |
| -------------------- |  ------------- |  --------- |-------- |
| `/api/v1/patients/`  | Permission     | Users      | Admin/staff 

##### GET

A **GET** request returns list of Patients with all of ther donations and medical employee resposible for register, also there is added dynamic field which returns information if the current Patient can donate.

| Filter | Type | Description |
| ------ | ---- | ----------- |
| **emailAddress** | String | Filter by email address *prefix* |
| **username** | String | Filter by username *prefix* |
| **firstName** | String | Filter by given name *prefix* |
| **lastName** | String | Filter by family name *prefix* |
| **nodeId** | Integer | Return only readers created at the given node ID |
| **subscription** | Integer | Return only readers subscribed to the subscription with the given ID |
