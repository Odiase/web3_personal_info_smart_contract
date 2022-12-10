// SPDX-License-Identifier: MIT

pragma solidity ^0.8;

contract PersonalInfo{

    struct HouseAddress {
        string location;
    }

    struct Person{
        string name;
        uint256 phone_number;
        HouseAddress residence;
    }

    Person[] public people;
    mapping(string => Person) public name_to_person;
    mapping(string => bool) public person_exists;

    function create_person(string memory name, uint256 phone_number, string memory residence) public {
        //check if a user with this name already exists
        require(person_exists[name] == false, "A User With This Username Already Exists.");

        // creating the struct instances
        HouseAddress memory residence_obj = HouseAddress(residence);
        Person memory person_obj = Person(name, phone_number, residence_obj);

        // adding object to array and mappings
        people.push(person_obj);
        name_to_person[name] = person_obj;
        person_exists[name] = true;
    }

    function get_person_info(string memory name) public view returns (Person memory) {
        // checking if such a name exists
        require(person_exists[name], "This Person Doesn't Exists!");

        //getting the person info
        Person memory person_obj = name_to_person[name];
        return person_obj;
    }

    function delete_person(string memory name) public {
        // checking if the person exists
        require(person_exists[name], "This Person Doesn't Exists!");

        // deleting person record
        delete name_to_person[name];
        delete person_exists[name];
    }
}
