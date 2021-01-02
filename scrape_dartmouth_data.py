from bs4 import BeautifulSoup
import requests
import csv

source = requests.get('http://dartmouth.smartcatalogiq.com/current/orc/Departments-Programs-Undergraduate').text
soup = BeautifulSoup(source, 'lxml')
deptList = soup.find('div', class_='toc').ul.find('li', class_='hasChildren active').ul.find_all('li', class_='hasChildren')

csvFile = open('Dartmouth-Course-Catalog.csv', 'w', newline='')
csvWriter = csv.writer(csvFile)
csvWriter.writerow(['department', 'code', 'number', 'title', 'description', 'url'])

for dept in deptList:
    deptName = dept.a.text
    deptURL = dept.a['href']

    # print('DEPARTMENT NAME IS: ' + deptName)

    deptSource = requests.get(f'http://dartmouth.smartcatalogiq.com{deptURL}').text
    deptSoup = BeautifulSoup(deptSource, 'lxml')

    subDeptList = deptSoup.find('li', class_='hasChildren active').ul.find('li', class_='hasChildren active').ul.find_all('li', class_='hasChildren')

    for subDept in subDeptList:
        subDeptName = subDept.a.text
        subDeptURL = 'http://dartmouth.smartcatalogiq.com' + subDept.a['href']

        # print('SUB DEPARTMENT NAME IS: ' + subDeptName)
        # print()

        coursesSource = requests.get(subDeptURL).text
        coursesSoup = BeautifulSoup(coursesSource, 'lxml')

        courses = coursesSoup.find('div', class_='toc').find('li', class_='hasChildren active')\
            .find('li', class_='hasChildren active').find('li', class_='hasChildren active').ul.find_all('li')

        for course in courses:
            courseCode = course.a.text.strip()
            courseURL = 'http://dartmouth.smartcatalogiq.com' + course.a['href']

            # print('COURSE CODE IS: ' + courseCode)
            # print(courseCode.split(' ')[0])
            # print(courseCode.split(' ')[1])

            courseSource = requests.get(courseURL).text
            courseSoup = BeautifulSoup(courseSource, 'lxml').find('div', id='main')

            try:
                courseName = courseSoup.h1.text.strip().split(' ')[2:]
                courseName = ' '.join(courseName).strip()
                # print('COURSE NAME IS: ' + courseName)
            except Exception as e:
                courseName = None
                # print('COURSE NAME IS:                                    NONEXISTENT NONEXISTENT NONEXISTENTNONEXISTENTNONEXISTENT NONEXISTENT NONEXISTENT NONEXISTENTNONEXISTENT NONEXISTENT NONEXISTENT')

            try:
                courseDesc = courseSoup.find('div', class_='desc').text.strip()
                # print('COURSE DESCRIPTION IS: ' + courseDesc)
            except Exception as e:
                courseDesc = None
                # print('COURSE DESCRIPTION IS:                              NONEXISTENT NONEXISTENT NONEXISTENT NONEXISTENT NONEXISTENT NONEXISTENT NONEXISTENT NONEXISTENT NONEXISTENT NONEXISTENT ')

            try:
                csvWriter.writerow([deptName, courseCode.split(' ')[0], courseCode.split(' ')[1], courseName, courseDesc, courseURL])
            except Exception as e:
                print('DID NOT OUTPUT PROPERLY')
                print(deptName)
                print(courseCode.split(' ')[0])
                print(courseCode.split(' ')[1])
                print(courseName)
                print(courseDesc)
                print(courseURL)
                print()

            # print()

csvFile.close()

    # print()
    # print('___________________________________________________________________________________________________________'
    #       '___________________________________________________________________________________________')
    # print()

# MODEL FOR DOCUMENT
# DONE	departmentName - Computer Science
# DONE	departmentCode - COSC
# DONE	number - 10
# DONE	title - Object Oriented Programming
# DONE	description - "..."
# DONE	link - http://dartmouth.smartcatalogiq.com/current/orc/Departments-Programs-Undergraduate/Cognitive-Science/COGS-Cognitive-Science/COGS-1


# WE'VE GOT A PROBLEM: GET RID OF TUCK UNDERGRADUATE
# WE'VE GOT A PROBLEM: GET RID OF WGSS
# WE'VE GOT A PROBLEM: GET RID OF ETHICS INSTITUTE
# WE'VE GOT A PROBLEM: GET RID OF LANGUAGE AND ADVANCED LANGUAGE STUDY ABROAD
# WE'VE GOT A PROBLEM: GET RID OF MINOR IN MATERIALS SCIENCE
# WE'VE GOT A PROBLEM: GET RID OF MEDIEVAL AND RENAISSANCE STUDIES
# WE'VE GOT A PROBLEM: GET RID OF PHYSICAL EDUCATION
# WE'VE GOT A PROBLEM: GET RID OF STUDENT INITIATED SEMINARS
# WE'VE GOT A PROBLEM: GET RID OF INSTITUTE FOR WRITING AND RHETORIC

