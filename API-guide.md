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

##### **GET**

Returns list of Patients with all of ther donations and medical employee resposible for register, also there is added dynamic field which returns information if the current Patient can donate.

| Filter                | lookups           | Description |
| --------------------- | ---------------- | ----------- |
| **id**                | in           | Django’s built-in lookup |
| **first_name**          | exact, icontains           | Django’s built-in lookup |
| **last_name**         | exact, icontains           | Django’s built-in lookup |
| **pesel**          | exact, icontains           | Django’s built-in lookup |
| **blood_group**            | exact, icontains          | Django’s built-in lookup |
| **gender**      | exact          | Django’s built-in lookup |
| **email**      | exact, icontains          | Django’s built-in lookup |
| **phone_number**      | exact, icontains          | Django’s built-in lookup |
| **date_of_register**      | exact, icontains, gt, gte, lt, lte, year, month, day          | Django’s built-in lookup |
| **registered_by**      | exact          | Django’s built-in lookup |
| **subscription**      | Integer          | Django’s built-in lookup |
| **subscription**      | Integer          | Django’s built-in lookup |
| **subscription**      | Integer          | Django’s built-in lookup |
