# Corey Humeston Homework 3 #

#Import sqlite3 so Python knows what we're using
import sqlite3

#Found this online from Kulkarni's tutorial for Python
#Creating a new variable and connecting it to the chinook.db with sqlite3
file = sqlite3.connect('chinook.db')
#Creating cursor variable
cursor = file.cursor()

#While loop that's always true
while 32 :
    print
    print "Please make a selection in the database: "
    print "1) Obtain Album Title(s) based on Artist Name "
    #Number 2 is Optional
    #print "2) Obtain Tracks of an Album Title "
    print "3) Purchase History for a Customer "
    print "4) Update Track Price - Individual "
    #This one is also optional - number 5
    #print "5) Update Track Price - Batch "
    print "6) Exit Program "

    #Prompting user for input (like the Scanner class in Java)
    userInput = input("Your selection: ")

    #Getting Album Titles from Artists' Name
    if userInput == 1 :
        #Setting a variable for Artists' Name
        userArtistInput = raw_input("What is the Artists' Name? ")
        cursor.execute('''
            SELECT albumTable.AlbumId, albumTable.Title
            FROM Album albumTable
            WHERE albumTable.ArtistId IN (
            SELECT artistTable.ArtistId
            FROM Artist artistTable
            WHERE artistTable.ArtistId = albumTable.ArtistId AND
            artistTable.Name = \"''' + userArtistInput + '\" )'
        )
        #Gives us a list unless the result set is empty
        rows = cursor.fetchall()
        #If no Artist names match a row, tell the user
        if rows == [] :
            print
            print "No albums are available for this artist."

        #Iterating through rows
        for row in rows :
            print
            #Returning Title and ID
            print "Album Title: " +  str(row[1]) + " / Album ID: " + str(row[0])

    #Purchase history for a customer
    elif userInput == 3 :
        #Setting a variable for user Customer ID
        userCustomerInput = raw_input("What is the Customers' ID? ")
        cursor.execute('''
            SELECT invoiceLineTable.Quantity, invoiceTable.InvoiceDate, trackTable.Name, albumTable.Title
            FROM Invoice invoiceTable, Track trackTable, Album albumTable, InvoiceLine invoiceLineTable
            WHERE invoiceTable.CustomerId = ''' + userCustomerInput + ''' 
            AND invoiceTable.InvoiceId = invoiceLineTable.InvoiceId
            AND invoiceLineTable.TrackId = trackTable.TrackId
            AND trackTable.AlbumId = albumTable.AlbumId'''
        )
        #Gives us a list unless the result set is empty
        rows = cursor.fetchall()
        #If no Customer ID is matched, tell the user
        if rows == [] :
            print
            print "There is no Customer in the database with that ID."

        #Iterating through rows
        for row in rows:
            #Returning track name, album name, quantity, and invoice date
            print "Track Name:" , row[2]
            print "Album Name:" , row[3]
            print "Quantity:" , row[0]
            print "Invoice Date:" , row[1]
            print

    #Updating individual track price
    elif userInput == 4 :
        #Setting a variable for user to enter so I can reprint it later
        userTrackInput = raw_input("What is the Tracks' ID? ")
        cursor.execute('''
            SELECT DISTINCT trackTable.UnitPrice, trackTable.Name
            FROM Track trackTable
            WHERE trackTable.TrackId = ''' + userTrackInput)
        #Gives us a list, but one row by one row
        row = cursor.fetchone()
        #If no Track ID is matched, tell the user
        if row == None :
            print
            print "There is no Track with that ID in the database."
        else :
            print
            print "Current unit price for this track is $" + str(row[0])

        #Asking user to update pricing of Track
        userTrackNewInput = raw_input("What should be the new price? $")
        cursor.execute(''' 
            UPDATE Track
            SET UnitPrice = ''' + userTrackNewInput + '''
            WHERE TrackId = ''' + userTrackInput)
        #Writing to File
        file.commit()
        #Checking if UPDATE and SET worked
        if file.total_changes > 0.0 :
            print
            print "Updated Track Price!"
            print
            print "Track, " + str(row[1]) + ", is now $" + userTrackNewInput
        else :
            print "Sorry, that is not a valid price tag."

    #Exit program
    elif userInput == 6 :
        print "Exiting program..."
        break


