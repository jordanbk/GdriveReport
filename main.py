from reports import assessment_1, assessment_2, assessment_3

def get_assessment_choice():
    """
    Prompts the user to select which assessment to run.
    
    Returns:
        int: The chosen assessment number.
    """
    print("Welcome to the Google Drive Reporting Tool!")
    print("Please choose which assessment to run:")
    print("(1) Assessment 1: Count files and folders at the root level")
    print("(2) Assessment 2: Recursively count all files and folders")
    print("(3) Assessment 3: Copy folder contents from source folder to destination folder")
    print("(4) Exit")

    while True:
        try:
            choice = int(input("Enter the assessment number (1, 2, 3, or 4 to Exit): "))
            if choice in [1, 2, 3, 4]:
                return choice
            else:
                print("Invalid choice. Please select 1, 2, 3, or 4.")
        except ValueError:
            print("Invalid input. Please enter a number.")

def get_folder_id():
    """
    Prompts the user to enter a Google Drive folder ID.
    
    Returns:
        str: The entered folder ID.
    """
    return input("Please enter the Google Drive folder ID (hint: 1cpo-7jgKSMdde-QrEJGkGxN1QvYdzP9V): ")

def get_source_folder_id():
    """
    Prompts the user to enter a source Google Drive folder ID to copy contents from.
    
    Returns:
        str: The entered folder ID.
    """
    return input("Please enter the source Google Drive folder ID to copy contents from (hint: 1cpo-7jgKSMdde-QrEJGkGxN1QvYdzP9V): ")


def get_destination_folder_id():
    """
    Prompts the user to enter a destination Google Drive folder ID to copy contents to.
    
    Returns:
        str: The entered folder ID.
    """
    return input("Please enter the Google Drive folder ID to copy contents to (hint: 1TjN_VohuoM0MaIzYp-z16nVDLiVoWWW1): ")

def main():
    """
    Main function that interacts with the user to select an assessment and run it.
    Loops until the user chooses to exit.
    """
    while True:
        # Get the user's assessment choice
        assessment_number = get_assessment_choice()

        # If the user chooses to exit, break the loop
        if assessment_number == 4:
            print("Exiting the tool. Thank you!")
            break

        # Execute the corresponding assessment based on the user's choice
        if assessment_number == 1:
            # Get the source folder ID
            folder_id = get_folder_id()
            print("Running Assessment 1...")
            assessment_1.count_files(folder_id)
        elif assessment_number == 2:
            # Get the source folder ID
            folder_id = get_folder_id()
            print("Running Assessment 2...")
            assessment_2.count_recursive(folder_id)
        elif assessment_number == 3:
            # Get the source folder ID
            folder_id = get_source_folder_id()
            # Get the destination folder ID
            destination_folder_id = get_destination_folder_id()
            print("Running Assessment 3...")
            assessment_3.copy_folder_contents(folder_id, destination_folder_id)

        # After the assessment finishes, ask the user if they want to run another assessment
        print("\nReport complete.")
        another = input("Would you like to run another assessment? (yes/no): ").lower()
        if another != 'yes':
            print("Exiting the tool. Thank you and good bye!")
            break

if __name__ == "__main__":
    main()