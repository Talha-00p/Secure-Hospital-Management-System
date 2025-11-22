"""
Assignment4 scaffold

This file lists the main steps and provides simple functions to recreate the demo steps.
Run `python db_init.py` to create the database and sample users, then run the Streamlit app:

    streamlit run "streamlit_app.py"

"""

def steps():
    print('1. Run db_init.py to create DB and sample data')
    print('2. Start the Streamlit app: streamlit run streamlit_app.py')
    print('3. Login as admin / Dr. Bob / Alice_recep using the sample credentials (passwords hashed)')
    print('4. Test anonymization, exports, and receptionist editing flow')

if __name__ == '__main__':
    steps()
