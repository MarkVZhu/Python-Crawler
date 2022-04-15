''' This program will perform a web scrape on TIMESJOBS web pages and extract the following Job information:
job name, company, location, job description, skills, more information (the address of the job web page)'''

from bs4 import BeautifulSoup 
import urllib.request
import datetime


# A Job class is created in order to create an object for each job instance and save the information as its attributes.
class Job:
    def __init__(self,name, company, location, job_des, skills, more_info):
        self.name = name
        self.company = company
        self.location = location
        self.job_des = job_des
        self.skills = skills
        self.more_info = more_info
    # This function creates a string include each job's attributes.
    def get_string(self):
        return "Job name: " + str(self.name) + "\nCompany: " + str(self.company) + "\nLocation: " + str(self.location) \
            + "\nJob description: " + str(self.job_des) + "\nRequired skills: " + str(self.skills) + "\nMore Info: " + self.more_info + "\n\n" + "*" * 80 + "\n"

# This function performs the scrape of TIMESJOB pages. It collets all jobs' information blocks in a page. 
# It takes one argument: job_type. The job_type means the type of job, such as java, php, and python here. 
def req_data(job_type):
    job_info = []
    try:
        source = urllib.request.urlopen(f"https://www.timesjobs.com/candidate/job-search.html?searchType=personalizedSearch&from=submit&txtKeywords={job_type}&txtLocation=")
        tag = BeautifulSoup(source.read(), "html.parser")
        print(f"Requiring {job_type} jobs, please wait a moment...")
    
        #This statment finds all blocks that includ job information
        jobs = tag.find_all('li', class_ = 'clearfix job-bx wht-shd-bx')
        #This for loop traverse every single job information block
        for job in jobs:
            job_info.append(Job(*req_individual_data(job)))
        return(job_info)
    except:
        print("Your retrieval request was unsuccessful.")
        
# This function finds particular information in one block
# and assigns each piece of information to a corresponding variable of a job object
def req_individual_data(job):
    job_name = job.header.h2.a.text.strip().replace('\r', '')
    company_name = job.find('h3', class_ = 'joblist-comp-name').text.replace('(More Jobs)', '').strip().replace('\r', '')
    location = job.find('ul', class_ = 'top-jd-dtl clearfix').findChild('span').text.strip().replace('\r', '')
    job_des = job.find('ul', class_ = 'list-job-dtl clearfix').findChild('li').text.strip().replace('\r', '').replace('\n', '').replace('Job Description:', '')        
    skills = job.find('span', class_ = 'srp-skills').text.strip().replace('  ,  ', ', ')
    address = job.header.h2.a['href']
    return(job_name, company_name, location, job_des, skills, address)
    
# This function performs a frequency count of all words in the different {job}info.txt file using the dictionary concept.
def word_freq(job_type):
    try:
        with open(f"{job_type}info.txt", "r") as f:
            content = f.read().split()
            job_dict = {}
            for word in content:
                if word in job_dict:
                    job_dict[word] += 1
                else:
                    job_dict[word] = 1
            print(f"The frequency of all word occurrences in {job_type}info.txt file is:\n", job_dict)
    except:
        print(f"File {job_type}info.txt does not exsit.")        

#This function calls req_individual_data function, and writes the retrieved data into a corresponding txt file
def get_job_data(job_type):
    with open(f"{job_type}info.txt", "w") as f:
        f.write('Job Type: ' + job_type + "   Time: " + datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%D %H:%M:%S') + \
            "\n\n" + "*" * 80 + "\n")
        for job in req_data(job_type):
            # Calling get_string method to create strings out of each job's attributes.
            each_job = job.get_string()
            f.write(each_job)
    print(f"Retrieval {job_type} job information complete. You can find the data in {job_type}info.txt.")

def main():
    #This list stores the types of job that user wants to retrieve. 
    job_intentions = ['python','java','php']
    print("Retrieving Job information from the TIMESJOBS and saving it in (job_type)info.txt file...")
    #Retrieve each job type in the job_intentions list 
    for job_type in job_intentions:
        get_job_data(job_type)
    
    #Checking the frequency of words in {job_type}info.txt file
    word_freq(job_intentions[0]) #This statement check pythoninfo.txt
    #word_freq(job_intentions[1]) #This statement check javainfo.txt
    #word_freq(job_intentions[2]) #This statement check phpinfo.txt

    print("Retrieval complete. Goodbye.")
    
if __name__ == "__main__":
    main()