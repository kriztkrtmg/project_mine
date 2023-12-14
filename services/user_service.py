import bcrypt
from models.user_model import dataResponse
from motor.motor_asyncio import AsyncIOMotorClient

class userServiceClass():
    def __init__(self) -> None:
        client = AsyncIOMotorClient('localhost', 27017)
        database = client.project_mine
        self.md_user = database.user

    async def pswd_generator(self, password):
        """Hash password generator

        Args:
            password (str): user entry password

        Returns:
            str, str: Returns hashed password and random generated salt
        """
        salt_value = bcrypt.gensalt()
        hashed_pswd = bcrypt.hashpw(password.encode("utf-8"), salt_value)
        return hashed_pswd.decode("utf-8"), salt_value.decode("utf-8")
    
    async def check_password(self, user_doc, password):
        """Checks user entry password with hashed password

        Args:
            user_doc (dict): user's document from database
            password (str): user entry password

        Returns:
            bool: returns true if password matched
        """
        return bcrypt.checkpw(password.encode("utf-8"), user_doc["security_key"].encode("utf-8"))

    async def register_user(self, data):
        """register user

        Args:
            data (dict): user information

        Returns:
            dataResponse: creates account if username and email are unique and returns success message
        """
        if await self.md_user.find_one({"_id":data.username}):
            return dataResponse(
                Status="Error",
                Message="Sorry, this username is taken. Please try a different one."
            )
        if await self.md_user.find_one({"email":data.email}):
            return dataResponse(
                Status="Error",
                Message="Email already in use. Please choose a different one."
            )
        hashed_pswd, salt_token = await self.pswd_generator(data.password)
        document = {
            "_id": data.username,
            "email": data.email,
            "security_key": hashed_pswd,
            "security_token": salt_token,
            "role": "Standard"
        }
        try:
            await self.md_user.insert_one(document)
            return dataResponse(Status="Success", Message="Account Registered")
        except Exception as exe:
            return dataResponse(Status="Error", Message=exe)
        
    async def login_user(self, data):
        """login user

        Args:
            data (dict): user login input

        Returns:
            dataResponse: if user authencation is correct, then user logged in successfully
        """
        search_query = {"$or": [{"_id": data.identity}, {"email": data.identity}]}
        doc = await self.md_user.find_one(search_query)
        if not doc:
            return dataResponse(Status="Error",Message="Username|Email not registered.")
        if await self.check_password(doc, data.password):
            return dataResponse(Status="Success",Message="User Logged In")
        return dataResponse(Status="Error",Message="Password Incorrect")

        
            
        
