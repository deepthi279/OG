from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import connection
import uuid


class clientsView(APIView):

    def get(self, request, *args, **kwargs):
        """Retrieve a client by Alias (GUID) or ClientId, or return all clients"""

        Alias = kwargs.get('Alias', None)
        client_id = kwargs.get('Client_id', None)

        query = ""
        params = []

        if Alias:
            query = "SELECT * FROM clients WHERE Alias = %s;"
            params = [Alias]
        elif client_id:
            query = "SELECT * FROM clients WHERE ClientId = %s;"
            params = [client_id]
        else:
            query = "SELECT * FROM clients;"

        try:
            with connection.cursor() as cursor:
                cursor.execute(query, params)
                rows = cursor.fetchall()
                columns = [col[0] for col in cursor.description]
                results = [dict(zip(columns, row)) for row in rows]

                if not results:
                    return Response({"message": "Client not found."}, status=status.HTTP_404_NOT_FOUND)

                # Return a single client if querying by ID or Alias
                if Alias or client_id:
                    return Response(results[0], status=status.HTTP_200_OK)

                # Return all clients
                return Response(results, status=status.HTTP_200_OK)

        except Exception as e:
            print(f"Error: {str(e)}")
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
   

    def post(self, request, *args, **kwargs):
        """Add a new client with a unique Alias (GUID)"""
        Alias = request.data.get('Alias')

        if not Alias:
            Alias = str(uuid.uuid4())  # Generate a GUID if Alias is not provided
        print('///////////////',Alias)
        # Check if Alias already exists
        check_Alias_query = "SELECT COUNT(*) FROM clients WHERE Alias = %s;"

        try:
            data = request.data
            with connection.cursor() as cursor:
                cursor.execute(check_Alias_query, [Alias])
                Alias_count = cursor.fetchone()[0]

            if Alias_count > 0:
                return Response({"error": "Alias must be unique."}, status=status.HTTP_400_BAD_REQUEST)

            # Insert the new client data into the database
            insert_query = """
                INSERT INTO clients (FirstName, MiddleName, LastName, Alias, Office, DOB, Gender, Status, Street, City, State, ZipCode, 
                                     MobilePhone, OtherPhone, Extension, Email, AddressNotes, ProfilePicture)  
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
            """
            with connection.cursor() as cursor:
                cursor.execute(insert_query, (
                    data.get('FirstName'), data.get('MiddleName'), data.get('LastName'), data.get('Alias'), 
                    data.get('Office'), data.get('DOB'), data.get('Gender'), data.get('Status'),
                    data.get('Street'), data.get('City'), data.get('State'), data.get('ZipCode'),
                    data.get('MobilePhone'), data.get('OtherPhone'), data.get('Extension'),
                    data.get('Email'), data.get('AddressNotes'), data.get('ProfilePicture')
                ))
                connection.commit()  # Ensure the data is committed to the database

            return Response({"message": "Client added successfully.", "Alias": Alias}, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, *args, **kwargs):
        """Update an existing client by Alias (GUID)"""
        Alias = request.data.get('Alias')
        if not Alias:
            return Response({"error": "Alias is required."}, status=status.HTTP_400_BAD_REQUEST)

        # Check if Alias already exists
        check_Alias_query = "SELECT COUNT(*) FROM clients WHERE Alias = %s AND ClientId != %s;"

        try:
            data = request.data
            with connection.cursor() as cursor:
                cursor.execute(check_Alias_query, [Alias, data.get('ClientId')])
                Alias_count = cursor.fetchone()[0]

            if Alias_count > 0:
                return Response({"error": "Alias must be unique."}, status=status.HTTP_400_BAD_REQUEST)

            # Update the client details
            update_query = """
                UPDATE clients
                SET FirstName=%s, MiddleName=%s, LastName=%s, Alias=%s, Office=%s, DOB=%s, Gender=%s, Status=%s, 
                    Street=%s, City=%s, State=%s, ZipCode=%s, MobilePhone=%s, OtherPhone=%s, Extension=%s, 
                    Email=%s, AddressNotes=%s, ProfilePicture=%s
                WHERE ClientId=%s;
            """
            with connection.cursor() as cursor:
                cursor.execute(update_query, (
                    data.get('FirstName'), data.get('MiddleName'), data.get('LastName'),data.get('Alias'), 
                    data.get('Office'), data.get('DOB'), data.get('Gender'), data.get('Status'),
                    data.get('Street'), data.get('City'), data.get('State'), data.get('ZipCode'),
                    data.get('MobilePhone'), data.get('OtherPhone'), data.get('Extension'), 
                    data.get('Email'), data.get('AddressNotes'), data.get('ProfilePicture'),
                    data.get('ClientId')
                ))

            return Response({"message": "Client updated successfully."}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, *args, **kwargs):
        """Delete a client by Alias (GUID)"""
        Alias = request.data.get('Alias')
        if not Alias:
            return Response({"error": "Alias is required."}, status=status.HTTP_400_BAD_REQUEST)

        delete_query = "DELETE FROM clients WHERE Alias = %s;"

        try:
            with connection.cursor() as cursor:
                cursor.execute(delete_query, [Alias])
                if cursor.rowcount == 0:
                    return Response({"message": "Client not found."}, status=status.HTTP_404_NOT_FOUND)

            return Response({"message": "Client deleted successfully."}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class ProviderView(APIView):
    
    def get(self, request, *args, **kwargs):
        """Retrieve all users"""
        query = "SELECT * FROM Provider;"
        try:
            with connection.cursor() as cursor:
                cursor.execute(query)
                rows = cursor.fetchall()
                if not rows:
                    return Response({"message": "No Provider found."}, status=status.HTTP_404_NOT_FOUND)
                columns = [col[0] for col in cursor.description]
                data = [dict(zip(columns, row)) for row in rows]
            return Response(data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, *args, **kwargs):
        """Add a new Provider"""
        query = """
            INSERT INTO Provider (first_name, middle_name, last_name, alias, job_title, office, department, type, hire_date, dob, gender, service_provider, status, email, profile_picture, street, city, state, zip_code, address_notes)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        """
        try:
            data = request.data
            with connection.cursor() as cursor:
                cursor.execute(query, (
                    data.get('first_name'), data.get('middle_name'), data.get('last_name'), data.get('alias'),
                    data.get('job_title'), data.get('office'), data.get('department'), data.get('type'),
                    data.get('hire_date'), data.get('dob'), data.get('gender'), data.get('service_provider'),
                    data.get('status'), data.get('email'), data.get('profile_picture'), data.get('street'),
                    data.get('city'), data.get('state'), data.get('zip_code'), data.get('address_notes')
                ))
            return Response({"message": "User added successfully."}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def put(self, request, *args, **kwargs):
        """Update an existing Provider"""
        query = """
            UPDATE Provider
            SET first_name=%s, middle_name=%s, last_name=%s, alias=%s, job_title=%s, office=%s, department=%s, 
                type=%s, hire_date=%s, dob=%s, gender=%s, service_provider=%s, status=%s, email=%s, 
                profile_picture=%s, street=%s, city=%s, state=%s, zip_code=%s, address_notes=%s
            WHERE Provider_id=%s;
        """
        try:
            data = request.data
            with connection.cursor() as cursor:
                cursor.execute(query, (
                    data.get('first_name'), data.get('middle_name'), data.get('last_name'), data.get('alias'),
                    data.get('job_title'), data.get('office'), data.get('department'), data.get('type'),
                    data.get('hire_date'), data.get('dob'), data.get('gender'), data.get('service_provider'),
                    data.get('status'), data.get('email'), data.get('profile_picture'), data.get('street'),
                    data.get('city'), data.get('state'), data.get('zip_code'), data.get('address_notes'),
                    data.get('user_id')
                ))
                if cursor.rowcount == 0:
                    return Response({"message": "Provider not found."}, status=status.HTTP_404_NOT_FOUND)
            return Response({"message": "Provider updated successfully."}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, *args, **kwargs):
        """Delete a user"""
        query = "DELETE FROM Users WHERE Provider_id = %s;"
        try:
            user_id = request.data.get('Provider_id')
            with connection.cursor() as cursor:
                cursor.execute(query, [user_id])
                if cursor.rowcount == 0:
                    return Response({"message": "User not found."}, status=status.HTTP_404_NOT_FOUND)
            return Response({"message": "Provider deleted successfully."}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

