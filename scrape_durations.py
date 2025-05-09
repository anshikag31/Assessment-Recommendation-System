import json
import requests
from bs4 import BeautifulSoup
import time
import re

# Manually define the assessments data here (as a list of dictionaries)
assessments = [
  {
    "assessment_name": "Account Manager Solution",
    "url": "https://www.shl.com/products/product-catalog/view/account-manager-solution/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Administrative Professional - Short Form",
    "url": "https://www.shl.com/products/product-catalog/view/administrative-professional-short-form/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Agency Manager Solution",
    "url": "https://www.shl.com/products/product-catalog/view/agency-manager-solution/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Apprentice + 8.0 Job Focused Assessment",
    "url": "https://www.shl.com/products/product-catalog/view/apprentice-8-0-job-focused-assessment-4261/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Apprentice 8.0 Job Focused Assessment",
    "url": "https://www.shl.com/products/product-catalog/view/apprentice-8-0-job-focused-assessment/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Bank Administrative Assistant - Short Form",
    "url": "https://www.shl.com/products/product-catalog/view/bank-administrative-assistant-short-form/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Bank Collections Agent - Short Form",
    "url": "https://www.shl.com/products/product-catalog/view/bank-collections-agent-short-form/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Bank Operations Supervisor - Short Form",
    "url": "https://www.shl.com/products/product-catalog/view/bank-operations-supervisor-short-form/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Bilingual Spanish Reservation Agent Solution",
    "url": "https://www.shl.com/products/product-catalog/view/bilingual-spanish-reservation-agent-solution/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Bookkeeping, Accounting, Auditing Clerk Short Form",
    "url": "https://www.shl.com/products/product-catalog/view/bookkeeping-accounting-auditing-clerk-short-form/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Branch Manager - Short Form",
    "url": "https://www.shl.com/products/product-catalog/view/branch-manager-short-form/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Cashier Solution",
    "url": "https://www.shl.com/products/product-catalog/view/cashier-solution/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Global Skills Development Report",
    "url": "https://www.shl.com/products/product-catalog/view/global-skills-development-report/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": ".NET Framework 4.5",
    "url": "https://www.shl.com/products/product-catalog/view/net-framework-4-5/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": ".NET MVC (New)",
    "url": "https://www.shl.com/products/product-catalog/view/net-mvc-new/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": ".NET MVVM (New)",
    "url": "https://www.shl.com/products/product-catalog/view/net-mvvm-new/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": ".NET WCF (New)",
    "url": "https://www.shl.com/products/product-catalog/view/net-wcf-new/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": ".NET WPF (New)",
    "url": "https://www.shl.com/products/product-catalog/view/net-wpf-new/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": ".NET XAML (New)",
    "url": "https://www.shl.com/products/product-catalog/view/net-xaml-new/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Accounts Payable (New)",
    "url": "https://www.shl.com/products/product-catalog/view/accounts-payable-new/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Accounts Payable Simulation (New)",
    "url": "https://www.shl.com/products/product-catalog/view/accounts-payable-simulation-new/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Accounts Receivable (New)",
    "url": "https://www.shl.com/products/product-catalog/view/accounts-receivable-new/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Accounts Receivable Simulation (New)",
    "url": "https://www.shl.com/products/product-catalog/view/accounts-receivable-simulation-new/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "ADO.NET (New)",
    "url": "https://www.shl.com/products/product-catalog/view/ado-net-new/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Adobe Experience Manager (New)",
    "url": "https://www.shl.com/products/product-catalog/view/adobe-experience-manager-new/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Adobe Photoshop CC",
    "url": "https://www.shl.com/products/product-catalog/view/adobe-photoshop-cc/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Aeronautical Engineering (New)",
    "url": "https://www.shl.com/products/product-catalog/view/aeronautical-engineering-new/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Aerospace Engineering (New)",
    "url": "https://www.shl.com/products/product-catalog/view/aerospace-engineering-new/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Agile Software Development",
    "url": "https://www.shl.com/products/product-catalog/view/agile-software-development/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": "7 min",
    "test_type": "Coding"
  },
  {
    "assessment_name": "Agile Testing (New)",
    "url": "https://www.shl.com/products/product-catalog/view/agile-testing-new/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "AI Skills",
    "url": "https://www.shl.com/products/product-catalog/view/ai-skills/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Amazon Web Services (AWS) Development (New)",
    "url": "https://www.shl.com/products/product-catalog/view/amazon-web-services-aws-development-new/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Android Development (New)",
    "url": "https://www.shl.com/products/product-catalog/view/android-development-new/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Angular 6 (New)",
    "url": "https://www.shl.com/products/product-catalog/view/angular-6-new/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "AngularJS (New)",
    "url": "https://www.shl.com/products/product-catalog/view/angularjs-new/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Apache Hadoop (New)",
    "url": "https://www.shl.com/products/product-catalog/view/apache-hadoop-new/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Apache Hadoop Extensions (New)",
    "url": "https://www.shl.com/products/product-catalog/view/apache-hadoop-extensions-new/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Apache HBase (New)",
    "url": "https://www.shl.com/products/product-catalog/view/apache-hbase-new/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Apache Hive (New)",
    "url": "https://www.shl.com/products/product-catalog/view/apache-hive-new/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Apache Kafka (New)",
    "url": "https://www.shl.com/products/product-catalog/view/apache-kafka-new/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Apache Pig (New)",
    "url": "https://www.shl.com/products/product-catalog/view/apache-pig-new/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Apache Spark (New)",
    "url": "https://www.shl.com/products/product-catalog/view/apache-spark-new/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "ASP .NET with C# (New)",
    "url": "https://www.shl.com/products/product-catalog/view/asp-net-with-c-new/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "ASP.NET 4.5",
    "url": "https://www.shl.com/products/product-catalog/view/asp-net-4-5/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Assessment and Development Center Exercises",
    "url": "https://www.shl.com/products/product-catalog/view/assessment-and-development-center-exercises/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Automata - Fix (New)",
    "url": "https://www.shl.com/products/product-catalog/view/automata-fix-new/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Automata - SQL (New)",
    "url": "https://www.shl.com/products/product-catalog/view/automata-sql-new/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Automata (New)",
    "url": "https://www.shl.com/products/product-catalog/view/automata-new/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Automata Data Science (New)",
    "url": "https://www.shl.com/products/product-catalog/view/automata-data-science-new/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Automata Data Science Pro (New)",
    "url": "https://www.shl.com/products/product-catalog/view/automata-data-science-pro-new/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Automata Front End",
    "url": "https://www.shl.com/products/product-catalog/view/automata-front-end/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": "30 min",
    "test_type": "Coding"
  },
  {
    "assessment_name": "Automata Pro (New)",
    "url": "https://www.shl.com/products/product-catalog/view/automata-pro-new/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Automata Selenium",
    "url": "https://www.shl.com/products/product-catalog/view/automata-selenium/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Automation Anywhere RPA Development (New)",
    "url": "https://www.shl.com/products/product-catalog/view/automation-anywhere-rpa-development-new/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Automotive Engineering (New)",
    "url": "https://www.shl.com/products/product-catalog/view/automotive-engineering-new/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Basic Biology (New)",
    "url": "https://www.shl.com/products/product-catalog/view/basic-biology-new/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Basic Computer Literacy (Windows 10) (New)",
    "url": "https://www.shl.com/products/product-catalog/view/basic-computer-literacy-windows-10-new/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Basic Statistics (New)",
    "url": "https://www.shl.com/products/product-catalog/view/basic-statistics-new/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Biochemistry (New)",
    "url": "https://www.shl.com/products/product-catalog/view/biochemistry-new/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Biotech Lab Techniques (New)",
    "url": "https://www.shl.com/products/product-catalog/view/biotech-lab-techniques-new/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "BizTalk (New)",
    "url": "https://www.shl.com/products/product-catalog/view/biztalk-new/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Business Communication (adaptive)",
    "url": "https://www.shl.com/products/product-catalog/view/business-communication-adaptive/",
    "remote_support": "Yes",
    "adaptive_support": "Yes",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Business Communications",
    "url": "https://www.shl.com/products/product-catalog/view/business-communications/",
    "remote_support": "Yes",
    "adaptive_support": "Yes",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "C Programming (New)",
    "url": "https://www.shl.com/products/product-catalog/view/c-programming-new/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "C# Programming (New)",
    "url": "https://www.shl.com/products/product-catalog/view/c-programming-new-4039/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "C++ Programming (New)",
    "url": "https://www.shl.com/products/product-catalog/view/c-programming-new-4122/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Cardiology and Diabetes Management (New)",
    "url": "https://www.shl.com/products/product-catalog/view/cardiology-and-diabetes-management-new/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Ceramic Engineering (New)",
    "url": "https://www.shl.com/products/product-catalog/view/ceramic-engineering-new/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Chemical Engineering (New)",
    "url": "https://www.shl.com/products/product-catalog/view/chemical-engineering-new/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Cisco AppDynamics (New)",
    "url": "https://www.shl.com/products/product-catalog/view/cisco-appdynamics-new/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Civil Engineering (New)",
    "url": "https://www.shl.com/products/product-catalog/view/civil-engineering-new/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Cloud Computing (New)",
    "url": "https://www.shl.com/products/product-catalog/view/cloud-computing-new/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "COBOL Programming (New)",
    "url": "https://www.shl.com/products/product-catalog/view/cobol-programming-new/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Computer Science (New)",
    "url": "https://www.shl.com/products/product-catalog/view/computer-science-new/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Contact Center Call Simulation (New)",
    "url": "https://www.shl.com/products/product-catalog/view/contact-center-call-simulation-new/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Conversational Multichat Simulation",
    "url": "https://www.shl.com/products/product-catalog/view/conversational-multichat-simulation/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Core Java (Advanced Level) (New)",
    "url": "https://www.shl.com/products/product-catalog/view/core-java-advanced-level-new/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Core Java (Entry Level) (New)",
    "url": "https://www.shl.com/products/product-catalog/view/core-java-entry-level-new/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Count Out The Money",
    "url": "https://www.shl.com/products/product-catalog/view/count-out-the-money/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "CSS3 (New)",
    "url": "https://www.shl.com/products/product-catalog/view/css3-new/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Culinary Skills (New)",
    "url": "https://www.shl.com/products/product-catalog/view/culinary-skills-new/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Customer Service Phone Simulation",
    "url": "https://www.shl.com/products/product-catalog/view/customer-service-phone-simulation/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Customer Service Phone Solution",
    "url": "https://www.shl.com/products/product-catalog/view/customer-service-phone-solution/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Cyber Risk (New)",
    "url": "https://www.shl.com/products/product-catalog/view/cyber-risk-new/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Data Entry (New)",
    "url": "https://www.shl.com/products/product-catalog/view/data-entry-new/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Data Entry Alphanumeric Split Screen - US",
    "url": "https://www.shl.com/products/product-catalog/view/data-entry-alphanumeric-split-screen-us/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Data Entry Numeric Split Screen - US",
    "url": "https://www.shl.com/products/product-catalog/view/data-entry-numeric-split-screen-us/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Data Entry Ten Key Split Screen",
    "url": "https://www.shl.com/products/product-catalog/view/data-entry-ten-key-split-screen/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Data Science (New)",
    "url": "https://www.shl.com/products/product-catalog/view/data-science-new/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Data Warehousing Concepts",
    "url": "https://www.shl.com/products/product-catalog/view/data-warehousing-concepts/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Dependability and Safety Instrument (DSI)",
    "url": "https://www.shl.com/products/product-catalog/view/dependability-and-safety-instrument-dsi/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Dermatology (New)",
    "url": "https://www.shl.com/products/product-catalog/view/dermatology-new/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Desktop Support (New)",
    "url": "https://www.shl.com/products/product-catalog/view/desktop-support-new/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Digital Advertising (New)",
    "url": "https://www.shl.com/products/product-catalog/view/digital-advertising-new/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Digital Readiness Development Report - IC",
    "url": "https://www.shl.com/products/product-catalog/view/digital-readiness-development-report/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Digital Readiness Development Report - Manager",
    "url": "https://www.shl.com/products/product-catalog/view/digital-readiness-development-report-manager/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Docker (New)",
    "url": "https://www.shl.com/products/product-catalog/view/docker-new/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Dojo (New)",
    "url": "https://www.shl.com/products/product-catalog/view/dojo-new/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Drupal (New)",
    "url": "https://www.shl.com/products/product-catalog/view/drupal-new/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "DSI v1.1 Interpretation Report",
    "url": "https://www.shl.com/products/product-catalog/view/dsi-v1-1-interpretation-report/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Econometrics (New)",
    "url": "https://www.shl.com/products/product-catalog/view/econometrics-new/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Economics (New)",
    "url": "https://www.shl.com/products/product-catalog/view/economics-new/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Electrical and Electronics Engineering (New)",
    "url": "https://www.shl.com/products/product-catalog/view/electrical-and-electronics-engineering-new/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Electrical Engineering (New)",
    "url": "https://www.shl.com/products/product-catalog/view/electrical-engineering-new/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Electronics & Telecommunications Engineering (New)",
    "url": "https://www.shl.com/products/product-catalog/view/electronics-and-telecommunications-engineering-new/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Electronics and Embedded Systems Engineering (New)",
    "url": "https://www.shl.com/products/product-catalog/view/electronics-and-embedded-systems-engineering-new/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Electronics and Semiconductor Engineering (New)",
    "url": "https://www.shl.com/products/product-catalog/view/electronics-and-semiconductor-engineering-new/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "English Comprehension (New)",
    "url": "https://www.shl.com/products/product-catalog/view/english-comprehension-new/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Enterprise Java Beans (New)",
    "url": "https://www.shl.com/products/product-catalog/view/enterprise-java-beans-new/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Enterprise Leadership Report 1.0",
    "url": "https://www.shl.com/products/product-catalog/view/enterprise-leadership-report/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Enterprise Leadership Report 2.0",
    "url": "https://www.shl.com/products/product-catalog/view/enterprise-leadership-report-2-0/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Entry Level Cashier Solution",
    "url": "https://www.shl.com/products/product-catalog/view/entry-level-cashier-solution/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Entry Level Customer Serv-Retail & Contact Center",
    "url": "https://www.shl.com/products/product-catalog/view/entry-level-customer-serv-retail-and-contact-center/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Entry Level Customer Service (General) Solution",
    "url": "https://www.shl.com/products/product-catalog/view/entry-level-customer-service-general-solution/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Entry Level Hotel Front Desk Solution",
    "url": "https://www.shl.com/products/product-catalog/view/entry-level-hotel-front-desk-solution/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Entry Level Sales Solution",
    "url": "https://www.shl.com/products/product-catalog/view/entry-level-sales-solution/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Entry Level Technical Support Solution",
    "url": "https://www.shl.com/products/product-catalog/view/entry-level-technical-support-solution/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "ETL Testing (New)",
    "url": "https://www.shl.com/products/product-catalog/view/etl-testing-new/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Executive Scenarios",
    "url": "https://www.shl.com/products/product-catalog/view/executive-scenarios/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Executive Scenarios Narrative Report",
    "url": "https://www.shl.com/products/product-catalog/view/executive-scenarios-narrative-report/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Executive Scenarios Profile Report",
    "url": "https://www.shl.com/products/product-catalog/view/executive-scenarios-profile-report/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "ExpressJS (New)",
    "url": "https://www.shl.com/products/product-catalog/view/expressjs-new/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Filing - Names (R1)",
    "url": "https://www.shl.com/products/product-catalog/view/filing-names-r1/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Filing - Numbers",
    "url": "https://www.shl.com/products/product-catalog/view/filing-numbers/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Financial Accounting (New)",
    "url": "https://www.shl.com/products/product-catalog/view/financial-accounting-new/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Financial and Banking Services (New)",
    "url": "https://www.shl.com/products/product-catalog/view/financial-and-banking-services-new/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Fire Engineering (New)",
    "url": "https://www.shl.com/products/product-catalog/view/fire-engineering-new/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Following Instructions v1 - UK (R1)",
    "url": "https://www.shl.com/products/product-catalog/view/following-instructions-v1-uk-r1/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Following Instructions v1 - US (R2)",
    "url": "https://www.shl.com/products/product-catalog/view/following-instructions-v1-us-r2/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Food and Beverage Services (New)",
    "url": "https://www.shl.com/products/product-catalog/view/food-and-beverage-services-new/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Food Science (New)",
    "url": "https://www.shl.com/products/product-catalog/view/food-science-new/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Front Office Management (New)",
    "url": "https://www.shl.com/products/product-catalog/view/front-office-management-new/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Fundamentals of Chemistry (New)",
    "url": "https://www.shl.com/products/product-catalog/view/fundamentals-of-chemistry-new/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Fundamentals of Physics (New)",
    "url": "https://www.shl.com/products/product-catalog/view/fundamentals-of-physics-new/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "General Diseases (New)",
    "url": "https://www.shl.com/products/product-catalog/view/general-diseases-new/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Geoinformatics Engineering (New)",
    "url": "https://www.shl.com/products/product-catalog/view/geoinformatics-engineering-new/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Geoscience Engineering (New)",
    "url": "https://www.shl.com/products/product-catalog/view/geoscience-engineering-new/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "GIT (New)",
    "url": "https://www.shl.com/products/product-catalog/view/git-new/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Global Skills Assessment",
    "url": "https://www.shl.com/products/product-catalog/view/global-skills-assessment/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Graduate Scenarios",
    "url": "https://www.shl.com/products/product-catalog/view/graduate-scenarios/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Graduate Scenarios Narrative Report",
    "url": "https://www.shl.com/products/product-catalog/view/graduate-scenarios-narrative-report/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Graduate Scenarios Profile Report",
    "url": "https://www.shl.com/products/product-catalog/view/graduate-scenarios-profile-report/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Hibernate (New)",
    "url": "https://www.shl.com/products/product-catalog/view/hibernate-new/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "HIPAA (Security)",
    "url": "https://www.shl.com/products/product-catalog/view/hipaa-security/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "HiPo Assessment Report 1.0",
    "url": "https://www.shl.com/products/product-catalog/view/hipo-assessment-report-1-0/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "HiPo Assessment Report 2.0",
    "url": "https://www.shl.com/products/product-catalog/view/hipo-assessment-report-2-0/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "HiPo Unlocking Potential Report 2.0",
    "url": "https://www.shl.com/products/product-catalog/view/hipo-unlocking-potential-report-2-0/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Housekeeping (New)",
    "url": "https://www.shl.com/products/product-catalog/view/housekeeping-new/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "HTML/CSS (New)",
    "url": "https://www.shl.com/products/product-catalog/view/htmlcss-new/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "HTML5 (New)",
    "url": "https://www.shl.com/products/product-catalog/view/html5-new/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Human Resources (New)",
    "url": "https://www.shl.com/products/product-catalog/view/human-resources-new/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "IBM DataStage (New)",
    "url": "https://www.shl.com/products/product-catalog/view/ibm-datastage-new/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "IBM Sterling Order Management System (New)",
    "url": "https://www.shl.com/products/product-catalog/view/ibm-sterling-order-management-system-new/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Industrial Engineering (New)",
    "url": "https://www.shl.com/products/product-catalog/view/industrial-engineering-new/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Informatica (Architecture) (New)",
    "url": "https://www.shl.com/products/product-catalog/view/informatica-architecture-new/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Informatica (Developer) (New)",
    "url": "https://www.shl.com/products/product-catalog/view/informatica-developer-new/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Instrumentation Engineering (New)",
    "url": "https://www.shl.com/products/product-catalog/view/instrumentation-engineering-new/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Interpersonal Communications",
    "url": "https://www.shl.com/products/product-catalog/view/interpersonal-communications/",
    "remote_support": "Yes",
    "adaptive_support": "Yes",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Interviewing and Hiring Concepts (U.S.)",
    "url": "https://www.shl.com/products/product-catalog/view/interviewing-and-hiring-concepts-u-s/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "iOS Development (New)",
    "url": "https://www.shl.com/products/product-catalog/view/ios-development-new/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "ITIL (IT Infrastructure Library) (New)",
    "url": "https://www.shl.com/products/product-catalog/view/itil-it-infrastructure-library-new/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Java 2 Platform Enterprise Edition 1.4 Fundamental",
    "url": "https://www.shl.com/products/product-catalog/view/java-2-platform-enterprise-edition-1-4-fundamental/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Java 8 (New)",
    "url": "https://www.shl.com/products/product-catalog/view/java-8-new/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Java Design Patterns (New)",
    "url": "https://www.shl.com/products/product-catalog/view/java-design-patterns-new/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Java Frameworks (New)",
    "url": "https://www.shl.com/products/product-catalog/view/java-frameworks-new/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Java Platform Enterprise Edition 7 (Java EE 7)",
    "url": "https://www.shl.com/products/product-catalog/view/java-platform-enterprise-edition-7-java-ee-7/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Java Web Services (New)",
    "url": "https://www.shl.com/products/product-catalog/view/java-web-services-new/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "JavaScript (New)",
    "url": "https://www.shl.com/products/product-catalog/view/javascript-new/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Jenkins (New)",
    "url": "https://www.shl.com/products/product-catalog/view/jenkins-new/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Job Control Language (New)",
    "url": "https://www.shl.com/products/product-catalog/view/job-control-language-new/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "jQuery (New)",
    "url": "https://www.shl.com/products/product-catalog/view/jquery-new/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Kubernetes (New)",
    "url": "https://www.shl.com/products/product-catalog/view/kubernetes-new/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Linux Administration (New)",
    "url": "https://www.shl.com/products/product-catalog/view/linux-administration-new/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Linux Operating System",
    "url": "https://www.shl.com/products/product-catalog/view/linux-operating-system/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Linux Programming (General)",
    "url": "https://www.shl.com/products/product-catalog/view/linux-programming-general/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Load Runner (New)",
    "url": "https://www.shl.com/products/product-catalog/view/load-runner-new/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Management Scenarios",
    "url": "https://www.shl.com/products/product-catalog/view/management-scenarios/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Managerial Scenarios Candidate Report",
    "url": "https://www.shl.com/products/product-catalog/view/managerial-scenarios-candidate-report/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Managerial Scenarios Narrative Report",
    "url": "https://www.shl.com/products/product-catalog/view/managerial-scenarios-narrative-report/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Managerial Scenarios Profile Report",
    "url": "https://www.shl.com/products/product-catalog/view/managerial-scenarios-profile-report/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Manual Testing (New)",
    "url": "https://www.shl.com/products/product-catalog/view/manual-testing-new/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Manufac. & Indust. - Mechanical & Vigilance 8.0",
    "url": "https://www.shl.com/products/product-catalog/view/mechanical-and-vigilance-focus-8-0/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Manufac. & Indust. - Safety & Dependability 8.0",
    "url": "https://www.shl.com/products/product-catalog/view/safety-and-dependability-focus-8-0/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Manufacturing & Industrial - Essential Focus 8.0",
    "url": "https://www.shl.com/products/product-catalog/view/essential-focus-8-0/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Manufacturing & Industrial - Mechanical Focus 8.0",
    "url": "https://www.shl.com/products/product-catalog/view/mechanical-focus-8-0/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Manufacturing & Industrial - Vigilance Focus 8.0",
    "url": "https://www.shl.com/products/product-catalog/view/vigilance-focus-8-0/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Marketing (New)",
    "url": "https://www.shl.com/products/product-catalog/view/marketing-new/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Maven (New)",
    "url": "https://www.shl.com/products/product-catalog/view/maven-new/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Mechanical Engineering (New)",
    "url": "https://www.shl.com/products/product-catalog/view/mechanical-engineering-new/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Mechatronics Engineering (New)",
    "url": "https://www.shl.com/products/product-catalog/view/mechatronics-engineering-new/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Medical Terminology (New)",
    "url": "https://www.shl.com/products/product-catalog/view/medical-terminology-new/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Metallurgical Engineering (New)",
    "url": "https://www.shl.com/products/product-catalog/view/metallurgical-engineering-new/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "MFS 360 Enterprise Leadership Report",
    "url": "https://www.shl.com/products/product-catalog/view/mfs-360-enterprise-leadership-report/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "MFS 360 UCF Group Report",
    "url": "https://www.shl.com/products/product-catalog/view/mfs-360-ucf-group-report/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "MFS 360 UCF Performance Potential Dev Tips Report",
    "url": "https://www.shl.com/products/product-catalog/view/mfs-360-ucf-performance-potential-dev-tips-report/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "MFS 360 UCF Standard Report",
    "url": "https://www.shl.com/products/product-catalog/view/mfs-360-ucf-standard-report/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Micro Focus Unified Functional Testing (New)",
    "url": "https://www.shl.com/products/product-catalog/view/micro-focus-unified-functional-testing-new/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Microservices (New)",
    "url": "https://www.shl.com/products/product-catalog/view/microservices-new/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Microsoft Dynamics Development (New)",
    "url": "https://www.shl.com/products/product-catalog/view/microsoft-dynamics-development-new/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Microsoft Excel 365 - Essentials (New)",
    "url": "https://www.shl.com/products/product-catalog/view/microsoft-excel-365-essentials-new/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Microsoft Excel 365 (New)",
    "url": "https://www.shl.com/products/product-catalog/view/microsoft-excel-365-new/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Microsoft Outlook 2013 (adaptive)",
    "url": "https://www.shl.com/products/product-catalog/view/microsoft-outlook-2013-adaptive/",
    "remote_support": "Yes",
    "adaptive_support": "Yes",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Microsoft PowerPoint 365 - Essentials (New)",
    "url": "https://www.shl.com/products/product-catalog/view/microsoft-powerpoint-365-essentials-new/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Microsoft SQL Server 2014 Programming",
    "url": "https://www.shl.com/products/product-catalog/view/microsoft-sql-server-2014-programming/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Microsoft Windows Server 2012 Administration",
    "url": "https://www.shl.com/products/product-catalog/view/microsoft-windows-server-2012-administration/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Microsoft Word 365 - Essentials (New)",
    "url": "https://www.shl.com/products/product-catalog/view/microsoft-word-365-essentials-new/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Microsoft Word 365 (New)",
    "url": "https://www.shl.com/products/product-catalog/view/microsoft-word-365-new/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Mineral Engineering (New)",
    "url": "https://www.shl.com/products/product-catalog/view/mineral-engineering-new/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Mining Engineering (New)",
    "url": "https://www.shl.com/products/product-catalog/view/mining-engineering-new/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Mobility (New)",
    "url": "https://www.shl.com/products/product-catalog/view/mobility-new/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Molecular Biology (New)",
    "url": "https://www.shl.com/products/product-catalog/view/molecular-biology-new/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "MongoDB (New)",
    "url": "https://www.shl.com/products/product-catalog/view/mongodb-new/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Motivation Questionnaire MQM5",
    "url": "https://www.shl.com/products/product-catalog/view/motivation-questionnaire-mqm5/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "MQ Candidate Motivation Report",
    "url": "https://www.shl.com/products/product-catalog/view/mq-candidate-motivation-report/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "MQ Employee Motivation Report",
    "url": "https://www.shl.com/products/product-catalog/view/mq-employee-motivation-report/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "MQ Motivation Report Pack",
    "url": "https://www.shl.com/products/product-catalog/view/mq-motivation-report-pack/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "MQ Profile",
    "url": "https://www.shl.com/products/product-catalog/view/mq-profile/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "MS Access (New)",
    "url": "https://www.shl.com/products/product-catalog/view/ms-access-new/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "MS Excel (New)",
    "url": "https://www.shl.com/products/product-catalog/view/ms-excel-new/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "MS Office Basic Computer Literacy (New)",
    "url": "https://www.shl.com/products/product-catalog/view/ms-office-basic-computer-literacy-new/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "MS Office Basic Computer Literacy (Sim) (New)",
    "url": "https://www.shl.com/products/product-catalog/view/ms-office-basic-computer-literacy-sim-new/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "MS PowerPoint (New)",
    "url": "https://www.shl.com/products/product-catalog/view/ms-powerpoint-new/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "MS Word (New)",
    "url": "https://www.shl.com/products/product-catalog/view/ms-word-new/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "MuleSoft Development (New)",
    "url": "https://www.shl.com/products/product-catalog/view/mulesoft-development-new/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Multitasking Ability",
    "url": "https://www.shl.com/products/product-catalog/view/multitasking-ability/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Networking and Implementation (New)",
    "url": "https://www.shl.com/products/product-catalog/view/networking-and-implementation-new/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Node.js (New)",
    "url": "https://www.shl.com/products/product-catalog/view/node-js-new/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Nursing (New)",
    "url": "https://www.shl.com/products/product-catalog/view/nursing-new/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Occupational Personality Questionnaire OPQ32r",
    "url": "https://www.shl.com/products/product-catalog/view/occupational-personality-questionnaire-opq32r/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Operations Management (New)",
    "url": "https://www.shl.com/products/product-catalog/view/operations-management-new/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "OPQ Candidate Plus Report",
    "url": "https://www.shl.com/products/product-catalog/view/opq-candidate-plus-report/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "OPQ Candidate Report 2.0",
    "url": "https://www.shl.com/products/product-catalog/view/opq-candidate-report-2-0/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "OPQ Emotional Intelligence Report",
    "url": "https://www.shl.com/products/product-catalog/view/opq-emotional-intelligence-report/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "OPQ Leadership Report",
    "url": "https://www.shl.com/products/product-catalog/view/opq-leadership-report/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "OPQ Manager Plus Report",
    "url": "https://www.shl.com/products/product-catalog/view/opq-manager-plus-report/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "OPQ Manager Plus Report 2.0",
    "url": "https://www.shl.com/products/product-catalog/view/opq-manager-plus-report-2-0/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "OPQ Maximising your Learning Report",
    "url": "https://www.shl.com/products/product-catalog/view/opq-maximising-your-learning-report/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "OPQ MQ Sales Report",
    "url": "https://www.shl.com/products/product-catalog/view/opq-mq-sales-report/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "OPQ Premium Plus Report",
    "url": "https://www.shl.com/products/product-catalog/view/opq-premium-plus-report/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "OPQ Premium Plus Report 2.0",
    "url": "https://www.shl.com/products/product-catalog/view/opq-premium-plus-report-2-0/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "OPQ Profile Report",
    "url": "https://www.shl.com/products/product-catalog/view/opq-profile-report/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "OPQ Team Impact Group Development Report",
    "url": "https://www.shl.com/products/product-catalog/view/opq-team-impact-group-development-report/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "OPQ Team Impact Individual Development Report",
    "url": "https://www.shl.com/products/product-catalog/view/opq-team-impact-individual-development-report/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "OPQ Team Impact Selection Report",
    "url": "https://www.shl.com/products/product-catalog/view/opq-team-impact-selection-report/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "OPQ Team Types & Leadership Styles Profile",
    "url": "https://www.shl.com/products/product-catalog/view/opq-team-types-and-leadership-styles-profile/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "OPQ Team Types and Leadership Styles Report",
    "url": "https://www.shl.com/products/product-catalog/view/opq-team-types-and-leadership-styles-report/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "OPQ UCF Development Action Planner Report 1.0",
    "url": "https://www.shl.com/products/product-catalog/view/opq-ucf-development-action-planner-report/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "OPQ UCF Development Action Planner Report 2.0",
    "url": "https://www.shl.com/products/product-catalog/view/opq-ucf-development-action-planner-report-2-0/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "OPQ Universal Competency Report 1.0",
    "url": "https://www.shl.com/products/product-catalog/view/opq-universal-competency-report/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "OPQ Universal Competency Report 2.0",
    "url": "https://www.shl.com/products/product-catalog/view/opq-universal-competency-report-2-0/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "OPQ User and Managers Report",
    "url": "https://www.shl.com/products/product-catalog/view/opq-user-and-managers-report/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "OPQ User Report",
    "url": "https://www.shl.com/products/product-catalog/view/opq-user-report/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Oracle DBA (Advanced Level) (New)",
    "url": "https://www.shl.com/products/product-catalog/view/oracle-dba-advanced-level-new/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Oracle DBA (Entry Level) (New)",
    "url": "https://www.shl.com/products/product-catalog/view/oracle-dba-entry-level-new/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Oracle PL/SQL (New)",
    "url": "https://www.shl.com/products/product-catalog/view/oracle-plsql-new/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Oracle WebLogic Server (New)",
    "url": "https://www.shl.com/products/product-catalog/view/oracle-weblogic-server-new/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Organic Chemistry (New)",
    "url": "https://www.shl.com/products/product-catalog/view/organic-chemistry-new/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Paint Technology (New)",
    "url": "https://www.shl.com/products/product-catalog/view/paint-technology-new/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Pediatrics (New)",
    "url": "https://www.shl.com/products/product-catalog/view/pediatrics-new/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Pega Development (New)",
    "url": "https://www.shl.com/products/product-catalog/view/pega-development-new/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Perl (New)",
    "url": "https://www.shl.com/products/product-catalog/view/perl-new/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Petrochemical Engineering (New)",
    "url": "https://www.shl.com/products/product-catalog/view/petrochemical-engineering-new/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Petroleum Engineering (New)",
    "url": "https://www.shl.com/products/product-catalog/view/petroleum-engineering-new/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Pharmaceutical Analysis (New)",
    "url": "https://www.shl.com/products/product-catalog/view/pharmaceutical-analysis-new/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Pharmaceutical Chemistry (New)",
    "url": "https://www.shl.com/products/product-catalog/view/pharmaceutical-chemistry-new/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Pharmaceutical Science (New)",
    "url": "https://www.shl.com/products/product-catalog/view/pharmaceutical-science-new/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Pharmaceutics (New)",
    "url": "https://www.shl.com/products/product-catalog/view/pharmaceutics-new/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Pharmacology (New)",
    "url": "https://www.shl.com/products/product-catalog/view/pharmacology-new/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "PHP (New)",
    "url": "https://www.shl.com/products/product-catalog/view/php-new/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "PJM Development Report",
    "url": "https://www.shl.com/products/product-catalog/view/pjm-development-report/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "PJM Selection Report",
    "url": "https://www.shl.com/products/product-catalog/view/pjm-selection-report/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Polymer Engineering (New)",
    "url": "https://www.shl.com/products/product-catalog/view/polymer-engineering-new/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Power Electronics and Drives (New)",
    "url": "https://www.shl.com/products/product-catalog/view/power-electronics-and-drives-new/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Power System Engineering (New)",
    "url": "https://www.shl.com/products/product-catalog/view/power-system-engineering-new/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Prism (New)",
    "url": "https://www.shl.com/products/product-catalog/view/prism-new/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Production and Industrial Engineering (New)",
    "url": "https://www.shl.com/products/product-catalog/view/production-and-industrial-engineering-new/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Production Engineering (New)",
    "url": "https://www.shl.com/products/product-catalog/view/production-engineering-new/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Programming Concepts",
    "url": "https://www.shl.com/products/product-catalog/view/programming-concepts/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Project Management (2013)",
    "url": "https://www.shl.com/products/product-catalog/view/project-management-2013/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Proofreading v1",
    "url": "https://www.shl.com/products/product-catalog/view/proofreading-v1/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Python (New)",
    "url": "https://www.shl.com/products/product-catalog/view/python-new/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "R Programming (New)",
    "url": "https://www.shl.com/products/product-catalog/view/r-programming-new/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "ReactJS (New)",
    "url": "https://www.shl.com/products/product-catalog/view/reactjs-new/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Reading Comprehension - English v1",
    "url": "https://www.shl.com/products/product-catalog/view/reading-comprehension-english-v1/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Reading Comprehension - Spanish v1",
    "url": "https://www.shl.com/products/product-catalog/view/reading-comprehension-spanish-v1/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Reading Comprehension v2",
    "url": "https://www.shl.com/products/product-catalog/view/reading-comprehension-v2/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "RemoteWorkQ",
    "url": "https://www.shl.com/products/product-catalog/view/remoteworkq/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "RemoteWorkQ Manager Report",
    "url": "https://www.shl.com/products/product-catalog/view/remoteworkq-manager-report/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "RemoteWorkQ Participant Report",
    "url": "https://www.shl.com/products/product-catalog/view/remoteworkq-participant-report/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "RESTful Web Services (New)",
    "url": "https://www.shl.com/products/product-catalog/view/restful-web-services-new/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Retail Sales and Service Simulation",
    "url": "https://www.shl.com/products/product-catalog/view/retail-sales-and-service-simulation/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Reviewing Forms - US (R1)",
    "url": "https://www.shl.com/products/product-catalog/view/reviewing-forms-us-r1/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Ruby (New)",
    "url": "https://www.shl.com/products/product-catalog/view/ruby-new/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Ruby on Rails (New)",
    "url": "https://www.shl.com/products/product-catalog/view/ruby-on-rails-new/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Sales & Service Phone Simulation",
    "url": "https://www.shl.com/products/product-catalog/view/sales-and-service-phone-simulation/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Sales & Service Phone Solution",
    "url": "https://www.shl.com/products/product-catalog/view/sales-and-service-phone-solution/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Sales Interview Guide",
    "url": "https://www.shl.com/products/product-catalog/view/sales-interview-guide/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Sales Profiler Cards",
    "url": "https://www.shl.com/products/product-catalog/view/sales-profiler-cards/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Sales Transformation 1.0 - Individual Contributor",
    "url": "https://www.shl.com/products/product-catalog/view/sales-transformation-report-individual-contributor/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Sales Transformation 2.0 - Individual Contributor",
    "url": "https://www.shl.com/products/product-catalog/view/salestransformationreport2-0-individualcontributor/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Sales Transformation Report 1.0 - Sales Manager",
    "url": "https://www.shl.com/products/product-catalog/view/sales-transformation-report-sales-manager/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Sales Transformation Report 2.0 - Sales Manager",
    "url": "https://www.shl.com/products/product-catalog/view/sales-transformation-report-2-0-sales-manager/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Salesforce Development (New)",
    "url": "https://www.shl.com/products/product-catalog/view/salesforce-development-new/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "SAP ABAP (Advanced Level) (New)",
    "url": "https://www.shl.com/products/product-catalog/view/sap-abap-advanced-level-new/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "SAP ABAP (Intermediate Level) (New)",
    "url": "https://www.shl.com/products/product-catalog/view/sap-abap-intermediate-level-new/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "SAP Basis (New)",
    "url": "https://www.shl.com/products/product-catalog/view/sap-basis-new/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "SAP Business Objects WebI (New)",
    "url": "https://www.shl.com/products/product-catalog/view/sap-business-objects-webi-new/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "SAP BW (Business Warehouse) (New)",
    "url": "https://www.shl.com/products/product-catalog/view/sap-bw-business-warehouse-new/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "SAP HCM (Human Capital Management) (New)",
    "url": "https://www.shl.com/products/product-catalog/view/sap-hcm-human-capital-management-new/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "SAP Hybris (New)",
    "url": "https://www.shl.com/products/product-catalog/view/sap-hybris-new/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "SAP Materials Management (New)",
    "url": "https://www.shl.com/products/product-catalog/view/sap-materials-management-new/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "SAP SD (Sales and Distribution) (New)",
    "url": "https://www.shl.com/products/product-catalog/view/sap-sd-sales-and-distribution-new/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Search Engine Optimization (New)",
    "url": "https://www.shl.com/products/product-catalog/view/search-engine-optimization-new/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Selenium (New)",
    "url": "https://www.shl.com/products/product-catalog/view/selenium-new/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Shell Scripting (New)",
    "url": "https://www.shl.com/products/product-catalog/view/shell-scripting-new/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "SHL Verify Interactive - Inductive Reasoning",
    "url": "https://www.shl.com/products/product-catalog/view/shl-verify-interactive-inductive-reasoning/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "SHL Verify Interactive – Deductive Reasoning",
    "url": "https://www.shl.com/products/product-catalog/view/shl-verify-interactive-deductive-reasoning/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "SHL Verify Interactive – Numerical Reasoning",
    "url": "https://www.shl.com/products/product-catalog/view/shl-verify-interactive-numerical-reasoning/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "SHL Verify Interactive G+",
    "url": "https://www.shl.com/products/product-catalog/view/shl-verify-interactive-g/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": "36 min",
    "test_type": "Coding"
  },
  {
    "assessment_name": "SHL Verify Interactive Numerical Calculation",
    "url": "https://www.shl.com/products/product-catalog/view/shl-verify-interactive-numerical-calculation/",
    "remote_support": "Yes",
    "adaptive_support": "Yes",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Siebel Development (New)",
    "url": "https://www.shl.com/products/product-catalog/view/siebel-development-new/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Smart Interview Live",
    "url": "https://www.shl.com/products/product-catalog/view/smart-interview-live/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Smart Interview Live Coding",
    "url": "https://www.shl.com/products/product-catalog/view/smart-interview-live-coding/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Smart Interview On Demand",
    "url": "https://www.shl.com/products/product-catalog/view/smart-interview-on-demand/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Social Media (New)",
    "url": "https://www.shl.com/products/product-catalog/view/social-media-new/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Software Business Analysis",
    "url": "https://www.shl.com/products/product-catalog/view/software-business-analysis/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "SonarQube (New)",
    "url": "https://www.shl.com/products/product-catalog/view/sonarqube-new/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Spelling (U.S.) (New)",
    "url": "https://www.shl.com/products/product-catalog/view/spelling-u-s-new/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Split Screen Typing Test - Form 1",
    "url": "https://www.shl.com/products/product-catalog/view/split-screen-typing-test-form-1/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Spring (New)",
    "url": "https://www.shl.com/products/product-catalog/view/spring-new/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "SQL (New)",
    "url": "https://www.shl.com/products/product-catalog/view/sql-new/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "SQL Server (New)",
    "url": "https://www.shl.com/products/product-catalog/view/sql-server-new/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "SQL Server Analysis Services (SSAS) (New)",
    "url": "https://www.shl.com/products/product-catalog/view/sql-server-analysis-services-%28ssas%29-%28new%29/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "SQL Server Integration Services (SSIS) (New)",
    "url": "https://www.shl.com/products/product-catalog/view/sql-server-integration-services-ssis-new/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "SQL Server Reporting Services (SSRS) (New)",
    "url": "https://www.shl.com/products/product-catalog/view/sql-server-reporting-services-ssrs-new/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Statistical Analysis System (New)",
    "url": "https://www.shl.com/products/product-catalog/view/statistical-analysis-system-new/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Struts (New)",
    "url": "https://www.shl.com/products/product-catalog/view/struts-new/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "SVAR - Spoken English (AUS)",
    "url": "https://www.shl.com/products/product-catalog/view/svar-spoken-english-aus/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "SVAR - Spoken English (Indian Accent)  (New)",
    "url": "https://www.shl.com/products/product-catalog/view/svar-spoken-english-indian-accent-new/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "SVAR - Spoken English (U.K.)",
    "url": "https://www.shl.com/products/product-catalog/view/svar-spoken-english-u-k/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "SVAR - Spoken English (US)  (New)",
    "url": "https://www.shl.com/products/product-catalog/view/svar-spoken-english-us-new/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "SVAR - Spoken French (Canadian) (New)",
    "url": "https://www.shl.com/products/product-catalog/view/svar-spoken-french-canadian-new/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "SVAR - Spoken French (European) (New)",
    "url": "https://www.shl.com/products/product-catalog/view/svar-spoken-french-european-new/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "SVAR - Spoken Spanish (Castilian) (New)",
    "url": "https://www.shl.com/products/product-catalog/view/svar-spoken-spanish-castilian-new/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "SVAR - Spoken Spanish (North American) (New)",
    "url": "https://www.shl.com/products/product-catalog/view/svar-spoken-spanish-north-american-new/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Swing (New)",
    "url": "https://www.shl.com/products/product-catalog/view/swing-new/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Tableau (New)",
    "url": "https://www.shl.com/products/product-catalog/view/tableau-new/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Telecommunications Engineering (New)",
    "url": "https://www.shl.com/products/product-catalog/view/telecommunications-engineering-new/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Teradata Development (New)",
    "url": "https://www.shl.com/products/product-catalog/view/teradata-development-new/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Time Management (U.S.)",
    "url": "https://www.shl.com/products/product-catalog/view/time-management-u-s/",
    "remote_support": "Yes",
    "adaptive_support": "Yes",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Training Development",
    "url": "https://www.shl.com/products/product-catalog/view/training-development/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Typing (New)",
    "url": "https://www.shl.com/products/product-catalog/view/typing-new/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "UiPath RPA Development (New)",
    "url": "https://www.shl.com/products/product-catalog/view/uipath-rpa-development-new/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Universal Competency Framework Interview Guide",
    "url": "https://www.shl.com/products/product-catalog/view/universal-competency-framework-interview-guide/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Universal Competency Framework Job profiling guide",
    "url": "https://www.shl.com/products/product-catalog/view/universal-competency-framework-job-profiling-guide/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Universal Competency Framework Profiler Cards (44)",
    "url": "https://www.shl.com/products/product-catalog/view/universal-competency-framework-profiler-cards-44/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "UNIX (New)",
    "url": "https://www.shl.com/products/product-catalog/view/unix-new/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "VB.NET (New)",
    "url": "https://www.shl.com/products/product-catalog/view/vb-net-new/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Verify - Deductive Reasoning",
    "url": "https://www.shl.com/products/product-catalog/view/verify-deductive-reasoning/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": "18 min",
    "test_type": "Coding"
  },
  {
    "assessment_name": "Verify - Following Instructions",
    "url": "https://www.shl.com/products/product-catalog/view/verify-following-instructions/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Verify - G+",
    "url": "https://www.shl.com/products/product-catalog/view/verify-g/",
    "remote_support": "Yes",
    "adaptive_support": "Yes",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Verify - General Ability Screen",
    "url": "https://www.shl.com/products/product-catalog/view/verify-general-ability-screen/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Verify - Inductive Reasoning (2014)",
    "url": "https://www.shl.com/products/product-catalog/view/verify-inductive-reasoning-2014/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Verify - Numerical Ability",
    "url": "https://www.shl.com/products/product-catalog/view/verify-numerical-ability/",
    "remote_support": "Yes",
    "adaptive_support": "Yes",
    "duration": "20 min",
    "test_type": "Coding"
  },
  {
    "assessment_name": "Verify - Technical Checking - Next Generation",
    "url": "https://www.shl.com/products/product-catalog/view/verify-technical-checking-next-generation/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Verify - Verbal Ability - Next Generation",
    "url": "https://www.shl.com/products/product-catalog/view/verify-verbal-ability-next-generation/",
    "remote_support": "Yes",
    "adaptive_support": "Yes",
    "duration": "15 min",
    "test_type": "Coding"
  },
  {
    "assessment_name": "Verify - Working with Information",
    "url": "https://www.shl.com/products/product-catalog/view/verify-working-with-information/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Verify G+ - Ability Test Report",
    "url": "https://www.shl.com/products/product-catalog/view/verify-g-ability-test-report/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Verify G+ - Candidate Report",
    "url": "https://www.shl.com/products/product-catalog/view/verify-g-candidate-report/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Verify Interactive Ability Report",
    "url": "https://www.shl.com/products/product-catalog/view/verify-interactive-ability-report/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Verify Interactive G+ Candidate Report",
    "url": "https://www.shl.com/products/product-catalog/view/verify-interactive-g-candidate-report/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Verify Interactive G+ Report",
    "url": "https://www.shl.com/products/product-catalog/view/verify-interactive-g-report/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Verify Interactive Process Monitoring",
    "url": "https://www.shl.com/products/product-catalog/view/verify-interactive-process-monitoring/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Virtual Assessment and Development Centers",
    "url": "https://www.shl.com/products/product-catalog/view/virtual-assessment-and-development-centers/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Visual Basic for Applications (New)",
    "url": "https://www.shl.com/products/product-catalog/view/visual-basic-for-applications-new/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Visual Comparison - UK",
    "url": "https://www.shl.com/products/product-catalog/view/visual-comparison-uk/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Visual Comparison - US",
    "url": "https://www.shl.com/products/product-catalog/view/visual-comparison-us/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "VLSI and Embedded Systems (New)",
    "url": "https://www.shl.com/products/product-catalog/view/vlsi-and-embedded-systems-new/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "What Is The Value - US",
    "url": "https://www.shl.com/products/product-catalog/view/what-is-the-value-us/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Workplace Administration Skills (New)",
    "url": "https://www.shl.com/products/product-catalog/view/workplace-administration-skills-new/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Workplace Health and Safety (New)",
    "url": "https://www.shl.com/products/product-catalog/view/workplace-health-and-safety-new/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "WriteX - Email Writing (Customer Service) (New)",
    "url": "https://www.shl.com/products/product-catalog/view/writex-email-writing-customer-service-new/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "WriteX - Email Writing (Managerial) (New)",
    "url": "https://www.shl.com/products/product-catalog/view/writex-email-writing-managerial-new/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "WriteX - Email Writing (Sales) (New)",
    "url": "https://www.shl.com/products/product-catalog/view/writex-email-writing-sales-new/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Written English v1",
    "url": "https://www.shl.com/products/product-catalog/view/written-english-v1/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Written Spanish",
    "url": "https://www.shl.com/products/product-catalog/view/written-spanish/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Zabbix (New)",
    "url": "https://www.shl.com/products/product-catalog/view/zabbix-new/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "360 Digital Report",
    "url": "https://www.shl.com/products/product-catalog/view/360-digital-report/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "360° Multi-Rater Feedback System (MFS)",
    "url": "https://www.shl.com/products/product-catalog/view/360-multi-rater-feedback-system-mfs/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Claims/Operations Supervisor Solution",
    "url": "https://www.shl.com/products/product-catalog/view/claimsoperations-supervisor-solution/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Contact Center Customer Service + 8.0",
    "url": "https://www.shl.com/products/product-catalog/view/contact-center-customer-service-8-0/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Contact Center Customer Service 8.0",
    "url": "https://www.shl.com/products/product-catalog/view/contact-center-customer-service-8-0-4269/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Contact Center Manager - Short Form",
    "url": "https://www.shl.com/products/product-catalog/view/contact-center-manager-short-form/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Contact Center Sales & Service + 8.0",
    "url": "https://www.shl.com/products/product-catalog/view/contact-center-sales-and-service-8-0/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Contact Center Sales & Service 8.0",
    "url": "https://www.shl.com/products/product-catalog/view/contact-center-sales-and-service-8-0-4268/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Contact Center Team Lead/Coach - Short Form",
    "url": "https://www.shl.com/products/product-catalog/view/contact-center-team-leadcoach-short-form/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Contact Centre Agent Solution - UK",
    "url": "https://www.shl.com/products/product-catalog/view/contact-centre-agent-solution-uk/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Customer Service - Short Form",
    "url": "https://www.shl.com/products/product-catalog/view/customer-service-short-form/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Customer Service - Short Form - UK",
    "url": "https://www.shl.com/products/product-catalog/view/customer-service-short-form-uk/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Customer Service with Sales - Short Form",
    "url": "https://www.shl.com/products/product-catalog/view/customer-service-with-sales-short-form/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Director - Short Form",
    "url": "https://www.shl.com/products/product-catalog/view/director-short-form/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "District/Regional Manager Solution",
    "url": "https://www.shl.com/products/product-catalog/view/districtregional-manager-solution/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Entry Level Cashier 7.1 (Americas)",
    "url": "https://www.shl.com/products/product-catalog/view/entry-level-cashier-7-1-%28americas%29/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Entry Level Cashier 7.1 (International)",
    "url": "https://www.shl.com/products/product-catalog/view/entry-level-cashier-7-1-%28international%29/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Entry Level Customer Service 7.1 (Americas)",
    "url": "https://www.shl.com/products/product-catalog/view/entry-level-customer-service-7-1-%28americas%29/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Entry Level Customer Service 7.1 (International)",
    "url": "https://www.shl.com/products/product-catalog/view/entry-level-customer-service-%28retail-and-cc%29-7-1/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Entry Level Customer Service 7.1 (South Africa)",
    "url": "https://www.shl.com/products/product-catalog/view/entry-level-customer-service-7-1-%28south-africa%29/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Entry level Sales 7.1 (Americas)",
    "url": "https://www.shl.com/products/product-catalog/view/entry-level-sales-7-1-%28americas%29/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Entry level Sales 7.1 (International)",
    "url": "https://www.shl.com/products/product-catalog/view/entry-level-sales-7-1/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Entry Level Sales Sift Out 7.1",
    "url": "https://www.shl.com/products/product-catalog/view/entry-level-sales-sift-out-7-1/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Event Sales Manager Solution",
    "url": "https://www.shl.com/products/product-catalog/view/event-sales-manager-solution/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Executive - Short Form",
    "url": "https://www.shl.com/products/product-catalog/view/executive-short-form/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Financial Professional - Short Form",
    "url": "https://www.shl.com/products/product-catalog/view/financial-professional-short-form/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Financial Services Representative Solution",
    "url": "https://www.shl.com/products/product-catalog/view/financial-services-representative-solution/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Front Desk Associate Solution",
    "url": "https://www.shl.com/products/product-catalog/view/front-desk-associate-solution/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Gaming Associate Solution",
    "url": "https://www.shl.com/products/product-catalog/view/gaming-associate-solution/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Gaming Manager Solution",
    "url": "https://www.shl.com/products/product-catalog/view/gaming-manager-solution/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "General Entry Level - All Industries 7.0 Solution",
    "url": "https://www.shl.com/products/product-catalog/view/general-entry-level-all-industries-7-0-solution/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "General Entry Level - All Industries 7.1 Solution",
    "url": "https://www.shl.com/products/product-catalog/view/general-entry-level-all-industries-7-1-solution/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "General Entry Level - All Industries 7.1(Americas)",
    "url": "https://www.shl.com/products/product-catalog/view/general-entry-level-all-industries-7-1%28americas%29/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "General Entry Level – Data Entry 7.0 Solution",
    "url": "https://www.shl.com/products/product-catalog/view/general-entry-level-data-entry-7-0-solution/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Graduate + 8.0 Job Focused Assessment",
    "url": "https://www.shl.com/products/product-catalog/view/graduate-8-0-job-focused-assessment/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": "30 min",
    "test_type": "Coding"
  },
  {
    "assessment_name": "Graduate 7.1 Job Focused Assessment",
    "url": "https://www.shl.com/products/product-catalog/view/graduate-7-1-job-focused-assessment/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Graduate 8.0 Job Focused Assessment",
    "url": "https://www.shl.com/products/product-catalog/view/graduate-8-0-job-focused-assessment-4228/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": "20 min",
    "test_type": "Coding"
  },
  {
    "assessment_name": "Guest Service Team 7.0 Solution",
    "url": "https://www.shl.com/products/product-catalog/view/guest-service-team-7-0-solution/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Guest Services Associate Solution",
    "url": "https://www.shl.com/products/product-catalog/view/guest-services-associate-solution/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Healthcare Aide 7.0 Solution",
    "url": "https://www.shl.com/products/product-catalog/view/healthcare-aide-7-0-solution/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Healthcare Call Center Agent Solution",
    "url": "https://www.shl.com/products/product-catalog/view/healthcare-call-center-agent-solution/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Healthcare Service Associate Solution",
    "url": "https://www.shl.com/products/product-catalog/view/healthcare-service-associate-solution/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Healthcare Support Specialist Solution",
    "url": "https://www.shl.com/products/product-catalog/view/healthcare-support-specialist-solution/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Home Health Aide Solution",
    "url": "https://www.shl.com/products/product-catalog/view/home-health-aide-solution/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Hospitality Manager Solution",
    "url": "https://www.shl.com/products/product-catalog/view/hospitality-manager-solution/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Host Solution",
    "url": "https://www.shl.com/products/product-catalog/view/host-solution/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Industrial - Entry Level 7.0 Solution",
    "url": "https://www.shl.com/products/product-catalog/view/industrial-entry-level-7-0-solution/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Industrial - Entry Level 7.1 (Americas)",
    "url": "https://www.shl.com/products/product-catalog/view/industrial-entry-level-7-1-%28americas%29/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Industrial - Entry Level 7.1 (International)",
    "url": "https://www.shl.com/products/product-catalog/view/industrial-entry-level-7-1-%28international%29/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Industrial - Professional and Skilled 7.0 Solution",
    "url": "https://www.shl.com/products/product-catalog/view/industrial-professional-and-skilled-7-0-solution/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Industrial - Semi-skilled 7.1 (Americas)",
    "url": "https://www.shl.com/products/product-catalog/view/industrial-semi-skilled-7-1-%28americas%29/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Industrial - Semi-skilled 7.1 (International)",
    "url": "https://www.shl.com/products/product-catalog/view/industrial-semi-skilled-7-1-%28international%29/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Industrial Professional and Skilled 7.1 (Americas)",
    "url": "https://www.shl.com/products/product-catalog/view/industrial-professional-and-skilled-7-1-%28americas%29/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Industrial Professional and Skilled 7.1 Solution",
    "url": "https://www.shl.com/products/product-catalog/view/industrial-professional-and-skilled-7-1-solution/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Installation and Repair Technician Solution",
    "url": "https://www.shl.com/products/product-catalog/view/installation-and-repair-technician-solution/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Insurance Account Manager Solution",
    "url": "https://www.shl.com/products/product-catalog/view/insurance-account-manager-solution/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Insurance Administrative Assistant Solution",
    "url": "https://www.shl.com/products/product-catalog/view/insurance-administrative-assistant-solution/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Insurance Agent Solution",
    "url": "https://www.shl.com/products/product-catalog/view/insurance-agent-solution/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Insurance Director Solution",
    "url": "https://www.shl.com/products/product-catalog/view/insurance-director-solution/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Insurance Sales Manager Solution",
    "url": "https://www.shl.com/products/product-catalog/view/insurance-sales-manager-solution/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Manager - Short Form",
    "url": "https://www.shl.com/products/product-catalog/view/manager-short-form/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Manager + 7.0 Solution",
    "url": "https://www.shl.com/products/product-catalog/view/manager-7-0-solution-3955/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Manager + 7.1 (Americas)",
    "url": "https://www.shl.com/products/product-catalog/view/manager-7-1-solution-4242/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Manager + 7.1 (International)",
    "url": "https://www.shl.com/products/product-catalog/view/manager-7-1-%28international%29/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Manager 7.0 Solution",
    "url": "https://www.shl.com/products/product-catalog/view/manager-7-0-solution/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Manager 7.1 (Americas)",
    "url": "https://www.shl.com/products/product-catalog/view/manager-7-1-%28americas%29/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Manager 7.1 (International)",
    "url": "https://www.shl.com/products/product-catalog/view/manager-7-1-solution/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Manager 8.0 JFA",
    "url": "https://www.shl.com/products/product-catalog/view/manager-8-0-jfa/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Manager 8.0+ JFA",
    "url": "https://www.shl.com/products/product-catalog/view/manager-8-0-jfa-4310/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Manufacturing Production Team Member",
    "url": "https://www.shl.com/products/product-catalog/view/manufacturing-production-team-member/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Manufacturing Skilled Maintenance Worker",
    "url": "https://www.shl.com/products/product-catalog/view/manufacturing-skilled-maintenance-worker/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Network Engineer/Analyst Solution",
    "url": "https://www.shl.com/products/product-catalog/view/network-engineeranalyst-solution/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Nurse Leader Solution",
    "url": "https://www.shl.com/products/product-catalog/view/nurse-leader-solution/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Nurse Solution",
    "url": "https://www.shl.com/products/product-catalog/view/nurse-solution/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Nursing Assistant Solution",
    "url": "https://www.shl.com/products/product-catalog/view/nursing-assistant-solution/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Personal Banker - Short Form",
    "url": "https://www.shl.com/products/product-catalog/view/personal-banker-short-form/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Phone Banker - Short Form",
    "url": "https://www.shl.com/products/product-catalog/view/phone-banker-short-form/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Prep/Line Cook Solution",
    "url": "https://www.shl.com/products/product-catalog/view/prepline-cook-solution/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Professional + 7.0 Solution",
    "url": "https://www.shl.com/products/product-catalog/view/professional-7-0-solution-3958/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Professional + 7.1 (Americas)",
    "url": "https://www.shl.com/products/product-catalog/view/professional-7-1-%28americas%29/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Professional + 7.1 (International)",
    "url": "https://www.shl.com/products/product-catalog/view/professional-7-1-solution/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Professional 7.0 Solution",
    "url": "https://www.shl.com/products/product-catalog/view/professional-7-0-solution/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Professional 7.1 (International)",
    "url": "https://www.shl.com/products/product-catalog/view/professional-7-1-solution-4247/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Professional 8.0 JFA",
    "url": "https://www.shl.com/products/product-catalog/view/professional-8-0-jfa/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Professional/Individual Contributor - Short Form",
    "url": "https://www.shl.com/products/product-catalog/view/professionalindividual-contributor-short-form/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Project Manager - Short Form",
    "url": "https://www.shl.com/products/product-catalog/view/project-manager-short-form/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Proof Operator - Processing Specialist -Short Form",
    "url": "https://www.shl.com/products/product-catalog/view/proof-operator-processing-specialist-short-form/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Reservation Agent Solution",
    "url": "https://www.shl.com/products/product-catalog/view/reservation-agent-solution/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Restaurant Manager Solution",
    "url": "https://www.shl.com/products/product-catalog/view/restaurant-manager-solution/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Restaurant Supervisor Solution",
    "url": "https://www.shl.com/products/product-catalog/view/restaurant-supervisor-solution/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Retail Consultant Solution",
    "url": "https://www.shl.com/products/product-catalog/view/retail-consultant-solution/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Retail Manager w/ Sales Solution",
    "url": "https://www.shl.com/products/product-catalog/view/retail-manager-w-sales-solution/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Retail Sales Associate Solution",
    "url": "https://www.shl.com/products/product-catalog/view/retail-sales-associate-solution/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Sales Director Solution",
    "url": "https://www.shl.com/products/product-catalog/view/sales-director-solution/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Sales Engineer Solution",
    "url": "https://www.shl.com/products/product-catalog/view/sales-engineer-solution/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Sales Manager Solution",
    "url": "https://www.shl.com/products/product-catalog/view/sales-manager-solution/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Sales Professional 7.0 Solution",
    "url": "https://www.shl.com/products/product-catalog/view/sales-professional-7-0-solution/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Sales Professional 7.1 (Americas)",
    "url": "https://www.shl.com/products/product-catalog/view/sales-professional-7-1-%28americas%29/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Sales Professional Solution",
    "url": "https://www.shl.com/products/product-catalog/view/sales-professional-solution/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Sales Representative Solution",
    "url": "https://www.shl.com/products/product-catalog/view/sales-representative-solution/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Sales Supervisor Solution",
    "url": "https://www.shl.com/products/product-catalog/view/sales-supervisor-solution/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Sales Support Specialist Solution",
    "url": "https://www.shl.com/products/product-catalog/view/sales-support-specialist-solution/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Senior Insurance Agent Solution",
    "url": "https://www.shl.com/products/product-catalog/view/senior-insurance-agent-solution/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Senior Sales Professional Solution",
    "url": "https://www.shl.com/products/product-catalog/view/senior-sales-professional-solution/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Server Solution",
    "url": "https://www.shl.com/products/product-catalog/view/server-solution/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Service Associate Solution",
    "url": "https://www.shl.com/products/product-catalog/view/service-associate-solution/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Service Supervisor Solution",
    "url": "https://www.shl.com/products/product-catalog/view/service-supervisor-solution/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Stock Clerk Solution",
    "url": "https://www.shl.com/products/product-catalog/view/stock-clerk-solution/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Store Manager 7.0 Solution",
    "url": "https://www.shl.com/products/product-catalog/view/store-manager-7-0-solution/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Store Manager 7.1 (Americas)",
    "url": "https://www.shl.com/products/product-catalog/view/store-manager-7-1-%28americas%29/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Store Manager 7.1 (International)",
    "url": "https://www.shl.com/products/product-catalog/view/store-manager-7-1-%28international%29/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Store Manager Solution",
    "url": "https://www.shl.com/products/product-catalog/view/store-manager-solution/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Supervisor - Short Form",
    "url": "https://www.shl.com/products/product-catalog/view/supervisor-short-form/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Supervisor 7.0 Solution",
    "url": "https://www.shl.com/products/product-catalog/view/supervisor-7-0-solution/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Supervisor 7.1 (Americas)",
    "url": "https://www.shl.com/products/product-catalog/view/supervisor-7-1-%28americas%29/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Supervisor 7.1 (International)",
    "url": "https://www.shl.com/products/product-catalog/view/supervisor-7-1-%28international%29/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Support Associate Solution",
    "url": "https://www.shl.com/products/product-catalog/view/support-associate-solution/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Support Supervisor Solution",
    "url": "https://www.shl.com/products/product-catalog/view/support-supervisor-solution/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Technical Sales Associate Solution",
    "url": "https://www.shl.com/products/product-catalog/view/technical-sales-associate-solution/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Technician/Technologist Solution",
    "url": "https://www.shl.com/products/product-catalog/view/techniciantechnologist-solution/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Technology Professional 8.0 Job Focused Assessment",
    "url": "https://www.shl.com/products/product-catalog/view/technology-professional-8-0-job-focused-assessment/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Telenurse Solution",
    "url": "https://www.shl.com/products/product-catalog/view/telenurse-solution/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Teller 7.0",
    "url": "https://www.shl.com/products/product-catalog/view/teller-7-0/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Teller with Sales - Short Form",
    "url": "https://www.shl.com/products/product-catalog/view/teller-with-sales-short-form/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Transcriptionist Solution",
    "url": "https://www.shl.com/products/product-catalog/view/transcriptionist-solution/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Workplace Safety - Individual 7.0 Solution",
    "url": "https://www.shl.com/products/product-catalog/view/workplace-safety-individual-7-0-solution/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Workplace Safety - Individual 7.1 (Americas)",
    "url": "https://www.shl.com/products/product-catalog/view/workplace-safety-individual-7-1-solution/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Workplace Safety - Team 7.0 Solution",
    "url": "https://www.shl.com/products/product-catalog/view/workplace-safety-team-7-0-solution/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Workplace Safety - Team 7.1 (Americas)",
    "url": "https://www.shl.com/products/product-catalog/view/workplace-safety-team-7-1-%28americas%29/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Workplace Safety - Team 7.1 (International)",
    "url": "https://www.shl.com/products/product-catalog/view/workplace-safety-team-7-1-solution/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  },
  {
    "assessment_name": "Workplace Safety Solution",
    "url": "https://www.shl.com/products/product-catalog/view/workplace-safety-solution/",
    "remote_support": "Yes",
    "adaptive_support": "No",
    "duration": None,
    "test_type": "Coding"
  }
]
def save_assessments(assessments):
    """Save the updated assessments data to JSON file."""
    cleaned = []
    for a in assessments:
        duration = a.get("duration", "Not specified")
        # Ensure duration is saved correctly (either int or meaningful string)
        if isinstance(duration, int):
            final_duration = duration
        elif isinstance(duration, str) and duration.lower() in ["untimed", "not specified"]:
            final_duration = duration
        else:
            final_duration = "Not specified"

        cleaned.append({
            "url": a["url"],
            "adaptive_support": a["adaptive_support"],
            "description": a.get("description", "Not mentioned"),
            "duration": final_duration,
            "remote_support": a["remote_support"],
            "test_type": a.get("test_type", [])
        })

    with open('assessments.json', 'w', encoding='utf-8') as f:
        json.dump({"recommended_assessments": cleaned}, f, indent=2, ensure_ascii=False)
    print("✅ Saved updated assessments to assessments.json")

def extract_duration_from_soup(soup):
    """Extract duration from the page soup. Returns 'Untimed', an integer, or 'Not mentioned'."""
    for tag in soup.find_all(['p', 'li', 'span', 'div', 'h1', 'h2', 'h3', 'h4', 'h5']):
        text = tag.get_text(strip=True).lower()

        # Handle "untimed"
        if 'approximate completion time in minutes' in text and 'untimed' in text:
            return "Untimed"
        
        # Handle "approx. 25"
        match = re.search(r'approximate completion time in minutes\s*=\s*approx\.?\s*(\d+)', text)
        if match:
            return int(match.group(1))

        # Handle "max 30"
        match = re.search(r'approximate completion time in minutes\s*=\s*max\s*(\d+)', text)
        if match:
            return int(match.group(1))

        # Handle "approximate completion time in minutes = 20"
        match = re.search(r'approximate completion time in minutes\s*=\s*(\d+)', text)
        if match:
            return int(match.group(1))

        # Handle other general time mentions like "20 min", "1 hour"
        match = re.search(r'(\d+)\s*(min|minute|hr|hour)', text)
        if match:
            return int(match.group(1))
    
    return "Not specified"

def extract_test_type_from_soup(soup):
    """Extract test types like 'Knowledge & Skills', etc."""
    text = soup.get_text(separator=' ', strip=True)
    match = re.search(r'Test Type[:\-]?\s*([A-Z ]+)', text)
    if match:
        codes = match.group(1).strip().split()
        code_map = {
            'A': 'Ability & Aptitude',
            'B': 'Biodata & Situational Judgement',
            'C': 'Competencies',
            'D': 'Development & 360',
            'E': 'Assessment Exercises',
            'K': 'Knowledge & Skills',
            'P': 'Personality & Behavior',
            'S': 'Simulations'
        }
        # Filter out unwanted 'R' and map valid codes
        return [code_map.get(code, code) for code in codes if code != 'R']
    return []

def extract_description_from_soup(soup):
    """Extract full meta description or fallback paragraph."""
    try:
        meta = soup.find("meta", attrs={"name": "description"})
        if meta and meta.get("content"):
            return meta["content"].strip()
        # Fallback: longest paragraph
        paragraphs = soup.find_all("p")
        if paragraphs:
            longest = max(paragraphs, key=lambda p: len(p.get_text(strip=True)))
            return longest.get_text(strip=True)
    except Exception:
        pass
    return "Description not found"

def update_assessments(assessments):
    """Scrape and update duration, test_type, and description."""
    for assessment in assessments:
        print(f"\n⏳ Scraping: {assessment['assessment_name']}")
        try:
            response = requests.get(assessment['url'], timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')

            # Extract duration
            duration = extract_duration_from_soup(soup)
            assessment['duration'] = duration
            print(f"⏱️ Duration: {duration} minutes")

            # Extract test type
            test_type = extract_test_type_from_soup(soup)
            assessment['test_type'] = test_type
            print(f"📄 Test Type: {test_type}")

            # Extract full description
            description = extract_description_from_soup(soup)
            assessment['description'] = description
            print(f"📝 Description:\n{description}\n")

        except Exception as e:
            print(f"❌ Error processing {assessment['url']}: {e}")
            assessment['duration'] = 0
            assessment['test_type'] = []
            assessment['description'] = "Error"

        time.sleep(1)

def main():
    if not assessments:
        print("⚠️ No assessments to update.")
        return
    update_assessments(assessments)
    save_assessments(assessments)

if __name__ == "__main__":
    main()