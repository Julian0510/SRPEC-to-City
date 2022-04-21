import pandas as pd


#Main function: Assigns votes for a particular candidate (column) to block groups
def createTable(col, sov, cty_conv):

    #covert to strings
    sov['srprec'] = sov['srprec'].astype(str)
    cty_conv['srprec'] = cty_conv['srprec'].astype(str)

    #Make sure each SRPREC_KEY has a 0 in front of it
    key_sans_zero = cty_conv[cty_conv["srprec"].str[0:1] != "0"]
    cty_conv.loc[cty_conv["srprec"].str[0:1] != "0", "srprec"] = "0" + cty_conv["srprec"]

    #Join the block-precinct conversions to the precinct results, this is the equivalent of an xlookup or vlookup
    merged_res = pd.merge(
        left=cty_conv,
        right=sov,
        on='srprec',
        how='left'
    )
    
    #Make sure that the 'tract', 'block' & fips_code are strings & length 6
    merged_res['city'] = merged_res['city'].astype(str)

    #Assign precinct votes to blocks - pctsrprec is % of registered voters in an srprec that are from a particular block
    col_cty_name = [x for x in col]
    for i in range(len(col_cty_name)):
        merged_res[col_cty_name[i]] = merged_res[col[i]] * (merged_res['n_in_city']/merged_res['n'])
    
    cty = merged_res.groupby("city")[col_cty_name].sum()    
    
    return cty



sov = pd.read_csv("https://raw.githubusercontent.com/Julian0510/SRPEC-to-City/main/2020/Placer/c061_g20_sov_data_by_g20_srprec.csv")
cty_conv = pd.read_csv("https://raw.githubusercontent.com/Julian0510/SRPEC-to-City/main/2020/Placer/c061_g20_srprec_to_city.csv")

col = []
print("Please ente the first column name")
colname= input()
col.append(colname)

while True:
    print("Do you have any other columns to add? (Y or N")
    cont= input()
    if cont == "Y":
        print("What is the next column you would like to assign?")
        colname = input()
        col.append(colname)
    elif cont == "N":
        break
    else:
        print("Please input either Y or N.")


cty = createTable(col, sov, cty_conv)
cty.to_csv("g20_cty_placer.csv")
print("Done!")

