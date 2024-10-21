from reports import assessment_1, assessment_2, assessment_3
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)


class GDriveReportingTool:
    def __init__(self):
        """
        Initialize the Google Drive Reporting Tool class.
        """
        self.assessment_number = None

    def get_assessment_choice(self):
        """
        Prompts the user to select which assessment to run.

        Returns:
            int: The chosen assessment number.
        """
        print(Fore.CYAN + "\nWelcome to the Google Drive Reporting Tool!")
        print(Fore.YELLOW + "\nPlease choose which assessment to run:")
        print(
            Fore.GREEN
            + "\n(1) "
            + Fore.WHITE
            + "Assessment 1: Count files and folders at the root level"
        )
        print(
            Fore.GREEN
            + "(2) "
            + Fore.WHITE
            + "Assessment 2: Recursively count all files and folders"
        )
        print(
            Fore.GREEN
            + "(3) "
            + Fore.WHITE
            + "Assessment 3: Copy folder contents from source folder to destination folder"
        )
        print(Fore.GREEN + "(4) " + Fore.RED + "Exit")

        while True:
            try:
                self.assessment_number = int(
                    input("Enter the assessment number (1, 2, 3, or 4 to Exit): ")
                )
                if self.assessment_number in [1, 2, 3, 4]:
                    return self.assessment_number
                else:
                    print("Invalid choice. Please select 1, 2, 3, or 4.")
            except ValueError:
                print("Invalid input. Please enter a number.")

    def get_folder_id(self):
        """
        Prompts the user to enter a Google Drive folder ID.

        Returns:
            str: The entered folder ID.
        """
        return input(
            "\nPlease enter the Google Drive folder ID (hint: 1cpo-7jgKSMdde-QrEJGkGxN1QvYdzP9V): "
        )

    def get_source_folder_id(self):
        """
        Prompts the user to enter a source Google Drive folder ID to copy contents from.

        Returns:
            str: The entered folder ID.
        """
        return input(
            "\nPlease enter the source Google Drive folder ID to copy contents from (hint: 1cpo-7jgKSMdde-QrEJGkGxN1QvYdzP9V): "
        )

    def get_destination_folder_id(self):
        """
        Prompts the user to enter a destination Google Drive folder ID to copy contents to.

        Returns:
            str: The entered folder ID.
        """
        return input(
            "\nPlease enter the Google Drive folder ID to copy contents to (hint: 1TjN_VohuoM0MaIzYp-z16nVDLiVoWWW1): "
        )

    def run_assessment(self):
        """
        Executes the chosen assessment based on the user's input.
        """
        while True:
            # Get the user's assessment choice
            self.get_assessment_choice()

            # If the user chooses to exit, break the loop
            if self.assessment_number == 4:
                print("Exiting the tool. Thank you!👋")
                break

            # Execute the corresponding assessment based on the user's input
            if self.assessment_number == 1:
                folder_id = self.get_folder_id()
                print(Fore.YELLOW + "\nRunning Assessment 1...")
                assessment_1.count_files(folder_id)
            elif self.assessment_number == 2:
                folder_id = self.get_folder_id()
                print(Fore.YELLOW + "\nRunning Assessment 2...")
                assessment_2.count_recursive(folder_id)
            elif self.assessment_number == 3:
                folder_id = self.get_source_folder_id()
                destination_folder_id = self.get_destination_folder_id()
                print(Fore.YELLOW + "\nRunning Assessment 3...")
                assessment_3.copy_folder_contents(folder_id, destination_folder_id)

            # After the assessment finishes, ask the user if they want to run another assessment
            print("\nReport complete!")
            another = input(
                "\nWould you like to run another assessment? (yes/no): "
            ).lower()
            if another != "yes":
                print("\nExiting the tool. Thank you and good bye! 👋")
                break


if __name__ == "__main__":
    tool = GDriveReportingTool()
    tool.run_assessment()
