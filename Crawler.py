from Base import BaseCrawler
import requests
from bs4 import BeautifulSoup
import logging

logger = logging.getLogger('__main__')


class UCB(BaseCrawler):
    Course_Page_Url = "https://www.queensu.ca/academic-calendar/arts-science/course-descriptions/"
    University = "Queens University"
    Abbreviation = "queenSU"
    University_Homepage = "https://www.queensu.ca/"

    # Below fields didn't find in the website
    Prerequisite = None
    References = None
    Scores = None
    Projects = "https://me.queensu.ca/Graduate/MEng/Projects.html"
    Professor_Homepage = "https://www.queensu.ca/english/people"

    def get_courses_of_department(self, department):
        a_element = department.find('a')
        Department_Name = a_element.text
        department_url = "https://www.queensu.ca" + a_element.get('href')
        Course_Homepage = department_url

        department_page_content = requests.get(department_url).text
        department_soup = BeautifulSoup(department_page_content, 'html.parser')

        courses = department_soup.find_all(class_='courseblock')

        return courses, Department_Name, Course_Homepage

    def get_course_data(self, course):
        Course_Title = course.find("span",{"class":"text col-7 detail-title margin--tiny text--semibold text--big"}).find("strong").text

        Unit_Count = course.find("span",{"class":"text detail-hours_html text--semibold text--big"}).find("strong").text
        Unit_Count = Unit_Count.split()[-1]

        Description = course.find("p",{"class":"courseblockextra noindent"}).text

        Objective = None
        Outcome = None
        Professor = None
        try:
            Required_Skills = course.find("span",{"class":"text detail-requirements"}).text[14:]
        except:
            Required_Skills = None
        
        return Course_Title, Unit_Count, Objective, Outcome, Professor, Required_Skills, Description

    def handler(self):
        html_content = requests.get(self.Course_Page_Url).text
        soup = BeautifulSoup(html_content, 'html.parser')

        departments = soup.find("div",{'class':'sitemap'}).find('ul').find_all('li')
        for department in departments:
            courses, Department_Name, Course_Homepage = self.get_courses_of_department(department)
            for course in courses:
                Course_Title, Unit_Count, Objective, Outcome, Professor, Required_Skills, Description = self.get_course_data(
                    course)

                self.save_course_data(
                    self.University, self.Abbreviation, Department_Name, Course_Title, Unit_Count,
                    Professor, Objective, self.Prerequisite, Required_Skills, Outcome, self.References, self.Scores,
                    Description, self.Projects, self.University_Homepage, Course_Homepage, self.Professor_Homepage
                )


if __name__ == "__main__":
    crawl = UCB()
    crawl.handler()