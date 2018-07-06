# Solving unmatched table of contents listings

Questions:

- Why would an Entry fail to match with a corresponding piece of content?
- Do some entry and link pairs not have matching text?
- Why are there more links than entries?
- Am I searching for the correct text?
- What do I need in order to investigate a particular pair?
	- Page number, from the toc entry
	- knowing where the corresponding link should be in the text. 
	- then determine whether a link was discovered

Currently I have a number of TOC Entries with `INTRODUCTION` or `CONCLUSION` as their text. What is the current situation?

How can I match each TOC Entry labeled `INTRODUCTION` with it's corresponding link?
_I could create lists for each text value, and pick in order based on matching text._


Reasons why entries aren't matching:
- whitespace is collapsed in link contents (happened with a `<br>` tag)
	- `AppendixTOCEntry: "Fair Debt Collection Practices & A Sample Letter to Debt Collection Agency"`
	- more carefully extract text to ensure whitespace does not collapse
	- `' '.join([s for s in elem.strings])`
	- use levenshtein
- whitespace is different between entry and link contents
	- `AppendixTOCEntry: "Department of Veterans Affairs “Notice to Department of Veterans Affairs of Veteran or Beneficiary Incarcerated in Penal Institution – VA Form 21-4193"`
	- normalize whitespace
	- replace `"\xa0"` with `" "`
	- use levenshtein
- text-based match is not unique
	- use order _and_ text to determine matches.

Reasons why links aren't matching:
- it is an orphaned link.



```
	ChapterTOCEntry: "INTRODUCTION"
	ChapterTOCEntry: "Pre-release Planning — Getting a California State ID or Driver License While Incarcerated"
	ChapterTOCEntry: "CONCLUSION"
	ChapterTOCEntry: "Introduction"
	ChapterTOCEntry: "How did Realignment Change the way parole revocation hearings work (as of July 1, 2013)?"
	ChapterTOCEntry: "CONCLUSION"
	ChapterTOCEntry: "Introduction"
	ChapterTOCEntry: "CONCLUSION"
	AppendixTOCEntry: "San Francisco Fair Chance Ordinance"
	ChapterTOCEntry: "INTRODUCTION"
	AppendixTOCEntry: "Rosen Bien Galvan & Grunfeld LLP, Where to Send your SSI Application When in Custody"
	AppendixTOCEntry: "Department Of Veterans Affairs “Information Regarding Apportionment Of Beneficiary's Award” – VA Form 21-0788"
	AppendixTOCEntry: "Department of Veterans Affairs “Application for Health Benefits – VA Form 10-10EZ"
	AppendixTOCEntry: "Department of Veterans Affairs “Notice to Department of Veterans Affairs of Veteran or Beneficiary Incarcerated in Penal Institution – VA Form 21-4193"
	AppendixTOCEntry: "Department of Defense “Application for Correction of Military Record” – DD Form 149"
	ChapterTOCEntry: "Are there certain types of jobs I can’t have because of my criminal record?"
	AppendixTOCEntry: "LA Fair Chance Hiring Initiative"
	ChapterTOCEntry: "INTRODUCTION"
	ChapterTOCEntry: "Restitution"
	AppendixTOCEntry: "Earnings Withholding Order (Judicial Council Form WG-002)"
	AppendixTOCEntry: "Employee Instructions (Wage Garnishment) (Judicial Council Form WG-003)"
	AppendixTOCEntry: "Claim of Exemption (Judicial Council Form EJ-160)"
	AppendixTOCEntry: "Exemptions from the Enforcement of Judgments (Judicial Council Form EJ-155)"
	AppendixTOCEntry: "Fair Debt Collection Practices & A Sample Letter to Debt Collection Agency"
	AppendixTOCEntry: "Consumer Financial Protection Bureau: To Get and Keep a Good Credit Score"
	ChapterTOCEntry: "Introduction"
	ChapterTOCEntry: "What is a criminal record?"
	ChapterTOCEntry: "What can I do to show the probate court judge that custody or visitation with me is in the “best interest of the child”?"
	ChapterTOCEntry: "Conclusion"
	ChapterTOCEntry: "INTRODUCTION"
	ChapterTOCEntry: "Conclusion"
	AppendixTOCEntry: "Ideas on Where to Go for Support from Root & Rebound’s Toolkit: My Education, My Freedom"
	ChapterTOCEntry: "INTRODUCTION"
	ChapterTOCEntry: "Which marijuana-related offenses did not change under Prop. 64?"
	ChapterTOCEntry: "Will the remedy remove my registration requirement?"
	ChapterTOCEntry: "Will the remedy remove my registration requirement?"
```

```
Unused links
	TOCLinkItem: "Pre-release Planning — Getting a California State ID or Driver License While Incarcerated"
	TOCLinkItem: "What if I want to live in a nursing home?"
	TOCLinkItem: "How did Realignment Change the way parole revocation hearings work (as of July 1, 2013)?"
	TOCLinkItem: "General Assistance and General Relief (GA/GR) provide cash assistance to adults who have little money, no sources of support, and who are not currently receiving any other public benefits. Every county in California runs its own GA or GR program, referred to in some counties (mostly in Northern California) as General Assistance (GA) and in other counties (mostly in Southern California) as General Relief (GR)."
	TOCLinkItem: "Every county has its own rules, including specific limits on the income and property you can have. Contact your county welfare agency for more details. For a list of county welfare agencies, see Appendix A on PG. 505."
	TOCLinkItem: "Maybe. Some counties have special rules and restrictions for people with drug-related criminal convictions or other violations, or for people who are suspected of having a warrant, being in violation of parole or probation, or fleeing to avoid prosecution for a crime. Contact your county welfare agency to ask about its local policy. For a directory of county welfare agencies, see Appendix A, PG. 505. If you believe that your county welfare agency is wrongly or unlawfully denying GA/GR benefits to you, you may call the following nonprofit organizations: Public Interest Law Project (PILP) at (510) 891-9794 or the Western Center on Law and Poverty (WCLP) at (213) 487-7211, for advice."
	TOCLinkItem: "You must apply for General Assistance/General Relief in person. If you have a disability that stops you from going into the county welfare office, you can request help. Contact your county welfare agency for details about the application process in your county. For a directory of county welfare agencies, see Appendix A, PG. 505. Note that some counties accept GA/GR applications only at specific offices, so if you are unsure about which office to go to, you should call the main county welfare office and ask."
	TOCLinkItem: "IMPORTANT INFORMATION ABOUT HOUSEHOLD SIZE: In calculating your benefits, CalWORKs may not count some people in your home as part of your family. Ask your county CalWORKs office for details on who will be included in the “household size.” Examples of people who may not count, even if they live with you, are anyone who: is receiving SSI benefits; is a noncitizen or does not have permanent legal presence in the U.S.; foster children receiving foster care payments; sponsored noncitizens who receive support from sponsors; any anyone who was sanctioned by the CalWORKs program."
	TOCLinkItem: "Contact your local county welfare agency to get an application form and start the application process. For a directory of county welfare agencies in California, see Appendix A, PG. 505 or visit the website: www.cwda.org/links/chsa.php."
	TOCLinkItem: "Important Update!CalWORKs and CalFresh Now Open to People with Prior Drug Felony Convictions"
	TOCLinkItem: "The process may vary by county. Generally, it involves filling out a form, providing documents, and having an interview. For details about how to apply in your county, contact the CalFresh office in your area. For a directory of county CalFresh offices, see Appendix A, on PG. 505. For information on how to apply for CalFresh benefits in your county, please call 1-877-847-3663. You can also apply online at http://benefitscal.org."
	TOCLinkItem: "In person: Visit your county social services office. (For a statewide directory, see Appendix A, on PG. 505) At the office, you can pick up the application form, get help filling it out, and submit it."
	TOCLinkItem: "By mail: Send your completed application form to: Covered California; P.O. Box 989725; West Sacramento, CA 95798-9725.."
	TOCLinkItem: "By fax: Fax your completed application form to: 1-888-329-3700."
	TOCLinkItem: "Get in-person help at a local county social services office (for a statewide list of offices, see Appendix A, PG. 505, or visit http://www.coveredca.com/faqs/)."
	TOCLinkItem: "Birthdates and Social Security Numbers (SSNs) of all household members. For Covered California, a “family” is defined as the person who files taxes as head of household, plus all dependents claimed on those taxes.Current income and latest tax return information for your household. You may be asked to follow up with documents proving your income. If you earn wages, acceptable proof may include: your most recent W-2, a recent pay stub, a letter from your employer on official office letterhead, or a copy of a check paid to you as wages. Information about any health insurance that you or any household member receives through a job."
	TOCLinkItem: "To find out if you’re eligible for full or partial health care coverage through Medi-Cal, contact your county welfare agency. For a statewide directory of county welfare agencies, see Appendix A, on PG. 505. You may also seek to apply using a paper application."
	TOCLinkItem: "If you think you qualify for Medi-Cal based on a disability, contact your county Medi-Cal office before you apply. Also, if you are homebound or living in an assisted care facility, you can ask to have a Medi-Cal representative visit you and help complete your application in person. For a statewide directory of county social services offices, see Appendix A, PG. 505."
	TOCLinkItem: "By phone: Call your county social services office to apply by phone. You can contact Covered California to ask for the number of your county social services office by calling Covered California at 1-800-300-1506 (TTY: 1-888-889-4500), or by visiting its website: http://www.coveredca.com/contact/."
	TOCLinkItem: "By mail: Send your completed application form to: Covered California; P.O. Box 989725; West Sacramento, CA 95798-9725."
	TOCLinkItem: "By fax: Fax your completed form to: 1-888-329-3700."
	TOCLinkItem: "Get in-person help at a local county social services office (for a statewide list of offices, see Appendix A, PG. 505, or visit http://www.dhcs.ca.gov/services/medi-cal/Pages/CountyOffices.aspx."
	TOCLinkItem: "You can find a listing of Medi-Cal approved certified enrollers at: http://www.coveredca.com/get-help/local/#null. Certified enrollers are community-based organizations that have Covered California and Medi-Cal approval to help applicants apply for health care."
	TOCLinkItem: "In some counties, you may be able to enroll in this program even if you aren’t getting GA/GR. Contact your local county welfare office to find out if it has an E&T program, what services it offers through this program, and if you qualify. For a statewide list of county welfare agencies, see Appendix A, on PG. 505."
	TOCLinkItem: "CalFresh E&T operates differently in each county. Call your local county welfare office to find out if your county has a CalFresh E&T program, and if so, how enrollment works. For a list of county welfare agencies, see Appendix A, on PG. 505."
	TOCLinkItem: "Appendix A"
	TOCLinkItem: "Where to Send Your SSI Application When in Custody"
	TOCLinkItem: ""
	TOCLinkItem: "Department of Veterans Affairs “Information Regarding Apportionment Of Beneficiary's Award” – VA Form 21-0788"
	TOCLinkItem: "Department of Veterans Affairs “Application for Health Benefits” – VA Form 10-10EZ"
	TOCLinkItem: "Department of Veterans Affairs “Notice to Department of Veterans Affairs of Veteran or Beneficiary Incarcerated in Penal Institution” – VA Form 21-4193"
	TOCLinkItem: "Department of Defense “Application for Correction of Military Record” – DD Form 149"
	TOCLinkItem: "Earnings Withholding Order(Judicial Council Form WG-002)"
	TOCLinkItem: "Employee Instructions(Wage Garnishment)(Judicial Council Form WG-003)"
	TOCLinkItem: "Claim of Exemption(Judicial Council Form EJ-160)"
	TOCLinkItem: "Exemptions from the Enforcement of Judgments(Judicial Council Form EJ-155)"
	TOCLinkItem: "Fair Debt Collection Practices &A Sample Letter to Debt Collection Agency"
	TOCLinkItem: "Steps To Get & Keep a Good Credit Score (Consumer Financial Protection Bureau)"
	TOCLinkItem: "IMPORTANT! Always follow the conditions of any Criminal Protective Orders, Personal Conduct No-Contact Orders, or Supervision Conditions against you. For more information, go to PG 737."
	TOCLinkItem: "Your past and current contact with your child."
	TOCLinkItem: ""
	TOCLinkItem: ""
	TOCLinkItem: ""
	TOCLinkItem: "To challenge a condition of state parole, you will likely have to file a CDCR Form 602 administrative appeal and Form 22 with the Parole Department. Read more about that process in the PAROLE & PROBATION CHAPTER at PG. 178."
	TOCLinkItem: "WHAT WILL I LEARN about courts?"
	TOCLinkItem: "LSPC also has a 2012 manual that has the forms you may need. You can find this manual at: www.prisonerswithchildren.org/wp-content/uploads/2013/08/Incarcerated-parents-version-12.11.12.pdf"
	TOCLinkItem: "Under state law, the judge should automatically make an order for you to be transported to these types of hearings. The court MUST send a copy of the “transport order” to the warden or sheriff of your facility at least 15 days before the date you need transportation. If you do not receive this order, or if you want to be transported to court for other dependency court hearings, you can write to the court to request such an order, or ask the attorney representing you to request one. The sheriff’s department in the county in which hearing takes place is responsible for arranging your transportation, but you may have to be proactive and follow up with your institution to make sure you are transported on time."
	TOCLinkItem: "IMPORTANT! If you are looking for information on guardianship in juvenile dependency court cases, where Child Protective Services (CPS) is involved, go to PG. 762 These two courts (probate vs. dependency) have different rules for deciding who can become a guardian and how their judges will look at criminal records."
	TOCLinkItem: "Can CPS remove my child from my care just because I have a criminal record?"
	TOCLinkItem: "To learn more about how a judge makes this decision about where to place a child, see below on PG. 757. For more information on the difference between guardianship, adoption and foster care see PG. 749."
	TOCLinkItem: "How will a dependency court judge decide where to place a child?"
	TOCLinkItem: "Yes, there are certain convictions that will automatically ban you from reconnecting with your child. See the chart on PG. 726 for more information."
	TOCLinkItem: "How your child’s records can be sealed."
	TOCLinkItem: "For more information and specific questions about being pregnant and giving birth while incarcerated, see Appendix H, PG. 817."
	TOCLinkItem: "Write the Prison Law Office directly at: Prison Law Office, General Delivery, San Quentin, CA 94964."
	TOCLinkItem: "Under the law, there is a difference between being biologically related to a child and having the legal right to decide what is best for the child. “Paternity” or “parentage” is a legal concept—not a biological one! This means that you can be the child’s biological parent but not the “legal parent,” OR you can be the child’s legal parent even if you are not the biological parent. There are specific legal rules for deciding whom the child’s legal parents are—in other words, rules for establishing paternity/parentage (these legal rules are also called “presumptions”)."
	TOCLinkItem: ""
	TOCLinkItem: "What will I learn in the domestic violence & restraining orders chapter?"
	TOCLinkItem: ""
	TOCLinkItem: "What is child custody mediation?"
	TOCLinkItem: "What happens in child custody mediation?"
	TOCLinkItem: "Who is the mediator in child custody mediation?"
	TOCLinkItem: "How do I find a mediator?"
	TOCLinkItem: "I do not speak English and/or English is not my first language. Can I get an interpreter for my child custody mediation appointment?"
	TOCLinkItem: "It depends on the court. If you need an interpreter, you can ask your mediator if he/she has any recommendations. Also be sure to ask if there will be a fee, and if there is a fee for an interpreter, whether or not it can be waived (removed)."
	TOCLinkItem: "Can the child custody mediators make recommendations about who gets custody and visitation?"
	TOCLinkItem: "Is child custody mediation confidential?"
	TOCLinkItem: "will we be forced to make an agreement in the child custody mediation appointment?"
	TOCLinkItem: "What happens after child custody mediation?"
	TOCLinkItem: "What can I do if the dependency court judge ended my reunification services, and I want to try again to reunite with my child?"
	TOCLinkItem: "What happens when my child is arrested?"
	TOCLinkItem: "Right after the arrest, what are my child’s rights?"
	TOCLinkItem: "If my child is arrested, what are my rights and responsibilities as a parent or guardian?"
	TOCLinkItem: "What to do if my child gets a Notice to Appear?"
	TOCLinkItem: "I got a notice saying that my child has a “detention hearing” in juvenile court. What does this mean, and what happens next?"
	TOCLinkItem: "What should I know about the 601 and 602 Petitions?"
	TOCLinkItem: "601 petitions are filed by the probation department and allege facts that are only illegal because the offender is a child. This includes things such as breaking curfew, skipping school, running away or disobeying parents. If the court finds a minor guilty of these offenses they will become what is known as a “status offender”."
	TOCLinkItem: "What should I know about my child’s detention hearing?"
	TOCLinkItem: "My child’s case has been sent to juvenile delinquency court. What happens next?"
	TOCLinkItem: "What kinds of hearings might my child have in juvenile court?"
	TOCLinkItem: "What can the court decide about my child?"
	TOCLinkItem: "That your child must be sent to the Division of Juvenile Justice (DJJ) of the California Dept. of Corrections and Rehabilitation (CDCR). This means he/she will spend 30-90 days in a reception center, which will determine your child’s education and treatment needs. Then he/she will be sent to a correctional facility or youth camp."
	TOCLinkItem: "My child’s case has been sent to adult court. Why did this happen, and what happens next?"
	TOCLinkItem: "Is there a way to make my child’s juvenile records disappear?"
	TOCLinkItem: "Being a New Mother While Incarcerated"
	TOCLinkItem: "Is there any way I can stay with my child after I give birth?"
	TOCLinkItem: "My sentencing judge recommended the Family Foundations program. What is it? What will happen?"
	TOCLinkItem: "Who is eligible to go to Family Foundations Program?"
	TOCLinkItem: "Who is not eligible for Family Foundations Program?"
	TOCLinkItem: "Who is eligible for CPMP?"
	TOCLinkItem: "What can stop me from being eligible for CPMP?"
	TOCLinkItem: "I am currently pregnant and in jail. Will my child be taken away from me?"
	TOCLinkItem: "What rights do I have to make sure that my child goes to a good home while I’m incarcerated?"
	TOCLinkItem: "What is the process for creating a placement plan? Will my facility or hospital help?"
	TOCLinkItem: "Where can I get help in establishing parentage?"
	TOCLinkItem: "IDEAS ON WHERE TO GO FOR SUPPORT – FROM ROOT & REBOUND’S TOOLKIT: MY EDUCATION, MY FREEDOM"
	TOCLinkItem: "Which marijuana-related offenses did not change under Prop. 64?"
	TOCLinkItem: "Generally, if you have served time in prison for a felony conviction, you do not qualify for expungement. However, the Prop. 64 law clearly says that offenses reduced to misdemeanors under Prop. 64 should be treated as misdemeanors “for all purposes.”  This language should mean (and courts hopefully will decide it does mean) they will be misdemeanors for purposes of expungement under Penal Code section 1203.4a. If you are in this situation, you should consult with an attorney for more information. You can contact the public defender’s office in the county where you were sentenced. If you have already had your conviction expunged, you still should be eligible for Prop. 64 relief if you satisfy all the requirements."
```
