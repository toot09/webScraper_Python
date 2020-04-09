import csv

def save_to_file(jobs):
  file = open("jobs.csv", mode="w")
  writer = csv.writer(file)
  #csv 첫 줄(해더) 생성.
  writer.writerow(["title","company","loation","link"])
  for job in jobs:
    writer.writerow(list(job.values()))
  return