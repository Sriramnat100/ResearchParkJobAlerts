from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import pandas as pd, time
from datetime import date, timedelta
from dotenv import load_dotenv
import os
from send_email import Email
from tinydb import TinyDB, Query
import hashlib




class ExtractListings:

    def __init__(self):
        
        load_dotenv()

        #time sensitive
        self.URL = "https://researchpark.illinois.edu/work-here/careers/"
        self.today_formated = self.formated(date.today())
        self.yesterday_formated = self.formated(date.today() - timedelta(days=1))


        #dbs
        self.db = TinyDB("sent_jobs.json")
        self.q = Query()
        self.email_db = TinyDB("emails.json")
        self.email_q = Query()

        #emails
        self.email_password = os.getenv("EMAIL_PASSWORD")



    #Code for formatting everything
    def formated(self,date):
        formatted = f"{date.month}.{date.day}.{str(date.year)[-2:]}"
        return formatted

    
    def formatmsg(self, val):
        if val:
            final_message = ""
            for job in val:
                final_message += (
                    f"📌 {job['title']}\n"
                    f"🏢 Company: {job['company']}\n"
                    f"📅 Posted: {job['date_posted']}\n"
                    f"🔗 Link: {job['link']}\n"
                    f"{'-'*50}\n"
                )
        else:
            final_message = "No new job listings found."
        
        return final_message


    #All the hash related stuff
    def get_job_hash(self, job):
        combo = f"{job['title']}|{job['company']}|{job['link']}"
        return hashlib.sha256(combo.encode()).hexdigest()

    def has_been_sent(self, job):
        h = self.get_job_hash(job)
        return self.db.contains(self.q.hash == h)

    def mark_as_sent(self, job):
        self.db.insert({'hash': self.get_job_hash(job)})

    def add_email(self, email):
        if not self.email_db.contains(self.email_q.address == email):
            self.email_db.insert({"address": email})

    def get_all_emails(self):
        return [entry["address"] for entry in self.email_db.all()]


    #Getting the lists of the jobs on the website
    def getListings(self):
        with sync_playwright() as p:
            #Launches a headless chromium browser
            browser = p.chromium.launch(headless=True)

            #opens a new tab and then goes to the URL that I give it for research park
            page = browser.new_page()
            page.goto(self.URL, timeout=60000)

            #Wait's until One job listing is posted 
            page.wait_for_selector("li.job-listing")

            # Scroll until everything is loaded
            prev_height = 0

            #Keeps scrolling until reaches end of the page
            while True:
                page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                time.sleep(1)
                curr_height = page.evaluate("document.body.scrollHeight")
                if curr_height == prev_height:
                    break
                prev_height = curr_height

            #Grabbing full page's HTML 
            soup = BeautifulSoup(page.content(), "html.parser")
            browser.close()

        # Parse jobs
        rows = []

        for card in soup.select("li.job-listing"):
            try:

                #Everything in title
                title_tag = card.select_one(".title-sec a")
                title = title_tag.get_text(strip=True)
                link = title_tag["href"]
                date = card.select_one(".posted-on").get_text(strip=True).replace("Posted", "")
                full_title_sec = card.select_one(".title-sec").get_text(strip=True)
                company = full_title_sec.replace(title, "").strip()



                if (str(date) == self.today_formated or str(date) == self.yesterday_formated):
                    
                    rows.append({
                        "title": title,
                        "company": company,
                        "date_posted": date,
                        "link": link,
                    })

                else:
                    break
            except Exception as e:
                print(f"Skipping a card due to error: {e}")


        return rows
    
    def sendEmails(self):

        #Getting the recent jobs from the listings
        jobs = self.getListings()
        to_send = []

        #Checking if jobs have been sent before
        for job in jobs:
            if not self.has_been_sent(job):
                to_send.append(job)
                self.mark_as_sent(job)
        
        email_list = self.get_all_emails()



        #If there are any new jobs go ahead and send them
        if (to_send):
            
            emaildraft = self.formatmsg(to_send)    
            emailer = Email(self.email_password)

            for address in email_list:
                emailer.send_email("kingicydiamond@gmail.com", address, "Research Park Internship Drop", emaildraft)
                print("email successfully sent")
        
        else:
            print("email not sent")

tester = ExtractListings()
tester.add_email("sriramnat123@gmail.com")
tester.add_email("lerak55333@ofacer.com")
tester.sendEmails()
        


   




