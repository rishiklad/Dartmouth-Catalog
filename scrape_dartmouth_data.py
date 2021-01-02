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

    deptSource = requests.get(f'http://dartmouth.smartcatalogiq.com{deptURL}').text
    deptSoup = BeautifulSoup(deptSource, 'lxml')

    subDeptList = deptSoup.find('li', class_='hasChildren active').ul.find('li', class_='hasChildren active').ul.find_all('li', class_='hasChildren')

    for subDept in subDeptList:
        subDeptName = subDept.a.text
        subDeptURL = 'http://dartmouth.smartcatalogiq.com' + subDept.a['href']

        coursesSource = requests.get(subDeptURL).text
        coursesSoup = BeautifulSoup(coursesSource, 'lxml')

        courses = coursesSoup.find('div', class_='toc').find('li', class_='hasChildren active')\
            .find('li', class_='hasChildren active').find('li', class_='hasChildren active').ul.find_all('li')

        for course in courses:
            courseCode = course.a.text.strip()
            courseURL = 'http://dartmouth.smartcatalogiq.com' + course.a['href']

            courseSource = requests.get(courseURL).text
            courseSoup = BeautifulSoup(courseSource, 'lxml').find('div', id='main')

            try:
                courseName = courseSoup.h1.text.strip().split(' ')[2:]
                courseName = ' '.join(courseName).strip()
            except Exception as e:
                courseName = None

            try:
                courseDesc = courseSoup.find('div', class_='desc').text.strip()
            except Exception as e:
                courseDesc = None

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


csvFile.close()
