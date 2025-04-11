from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import uuid
from django.db import connection


class clientsView(APIView):

    def get(self, request, *args, **kwargs):
        """Retrieve a client by Alias (GUID) or ClientId and return with ClientId"""
        client_id = request.query_params.get('ClientId')  # Retrieve ClientId from query params
        alias = request.query_params.get('Alias')  # Retrieve Alias from query params

        if not client_id and not alias:
            return Response({"error": "Either 'ClientId' or 'Alias' must be provided."}, status=status.HTTP_400_BAD_REQUEST)

        query = ""
        params = []

        if client_id:
            query = "SELECT * FROM clients WHERE ClientId = %s;"
            params = [client_id]
        elif alias:
            query = "SELECT * FROM clients WHERE Alias = %s;"
            params = [alias]

        try:
            with connection.cursor() as cursor:
                cursor.execute(query, params)
                row = cursor.fetchone()

                if not row:
                    return Response({"message": "Client not found."}, status=status.HTTP_404_NOT_FOUND)

                columns = [col[0] for col in cursor.description]
                data = dict(zip(columns, row))

                # Return the Client details
                return Response({
                    "ClientId": data.get("ClientId"),
                    "Alias": data.get("Alias"),
                    "FirstName": data.get("FirstName"),
                    "MiddleName": data.get("MiddleName"),
                    "LastName": data.get("LastName"),
                    "Office": data.get("Office"),
                    "DOB": data.get("DOB"),
                    "Gender": data.get("Gender"),
                    "Status": data.get("Status"),
                    "Street": data.get("Street"),
                    "City": data.get("City"),
                    "State": data.get("State"),
                    "ZipCode": data.get("ZipCode"),
                    "MobilePhone": data.get("MobilePhone"),
                    "OtherPhone": data.get("OtherPhone"),
                    "Extension": data.get("Extension"),
                    "Email": data.get("Email"),
                    "AddressNotes": data.get("AddressNotes"),
                    "ProfilePicture": data.get("ProfilePicture")
                }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, *args, **kwargs):
        """Add a new client with a unique Alias (GUID)"""
        alias = request.data.get('Alias')

        if not alias:
            alias = str(uuid.uuid4())  # Generate a GUID if Alias is not provided
        print('///////////////',alias)
        # Check if Alias already exists
        check_alias_query = "SELECT COUNT(*) FROM clients WHERE Alias = %s;"

        try:
            data = request.data
            with connection.cursor() as cursor:
                cursor.execute(check_alias_query, [alias])
                alias_count = cursor.fetchone()[0]

            if alias_count > 0:
                return Response({"error": "Alias must be unique."}, status=status.HTTP_400_BAD_REQUEST)

            # Insert the new client data into the database
            insert_query = """
                INSERT INTO clients (FirstName, MiddleName, LastName, Alias, Office, DOB, Gender, Status, Street, City, State, ZipCode, 
                                     MobilePhone, OtherPhone, Extension, Email, AddressNotes, ProfilePicture)  
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
            """
            with connection.cursor() as cursor:
                cursor.execute(insert_query, (
                    data.get('FirstName'), data.get('MiddleName'), data.get('LastName'), alias, 
                    data.get('Office'), data.get('DOB'), data.get('Gender'), data.get('Status'),
                    data.get('Street'), data.get('City'), data.get('State'), data.get('ZipCode'),
                    data.get('MobilePhone'), data.get('OtherPhone'), data.get('Extension'),
                    data.get('Email'), data.get('AddressNotes'), data.get('ProfilePicture')
                ))
                connection.commit()  # Ensure the data is committed to the database

            return Response({"message": "Client added successfully.", "Alias": alias}, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, *args, **kwargs):
        """Update an existing client by Alias (GUID)"""
        alias = request.data.get('Alias')
        if not alias:
            return Response({"error": "Alias is required."}, status=status.HTTP_400_BAD_REQUEST)

        # Check if Alias already exists
        check_alias_query = "SELECT COUNT(*) FROM clients WHERE Alias = %s AND ClientId != %s;"

        try:
            data = request.data
            with connection.cursor() as cursor:
                cursor.execute(check_alias_query, [alias, data.get('ClientId')])
                alias_count = cursor.fetchone()[0]

            if alias_count > 0:
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
                    data.get('FirstName'), data.get('MiddleName'), data.get('LastName'), alias, 
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
        alias = request.data.get('Alias')
        if not alias:
            return Response({"error": "Alias is required."}, status=status.HTTP_400_BAD_REQUEST)

        delete_query = "DELETE FROM clients WHERE Alias = %s;"

        try:
            with connection.cursor() as cursor:
                cursor.execute(delete_query, [alias])
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

