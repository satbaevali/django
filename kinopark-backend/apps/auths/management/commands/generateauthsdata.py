
from typing import Any
from random import choice,choices,randint
from datetime import datetime
#Django modules
from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password
#Project modules
from apps.auths.models import CustomUser

class Command(BaseCommand):

    EMAIL_DOMAIN=(
        'mail.ru',
        'gmail.com'
    )
    FULLNAME = (
        "Temirlan",
        "Ussipbek",
        "Abdresh ",
        "Akniet",
        "Ercin",
        "Erlik",
        "Aspan",
    )
    def __generate_users(self,user_count = 100)->None:
        USERPASSWORD = make_password("12345")
        create_user:list[CustomUser] = []
        create_befor:int = CustomUser.objects.count()
        
        i:int
        for i in range(user_count):
            full_name:str= " ".join(choices(self.FULLNAME, k=2))
            email:str = f"{full_name}@{choice(self.EMAIL_DOMAIN)}"
            create_user.append(
                CustomUser(
                    full_name = full_name,
                    email= email,
                    password = USERPASSWORD
                )
            ) 
        CustomUser.objects.bulk_create(create_user,ignore_conflicts=True)
        create_after:int = CustomUser.objects.count()
        
        self.stdout.write(
            self.style.SUCCESS(
                f"Created {create_after - create_befor} CustomUser" 
            )
        )




    def handle(self, *args:tuple[Any,...], **kwargs:dict[str,Any])->None:
        start_time:datetime = datetime.now()
        
        self.__generate_users(user_count=100)
        
        self.stdout.write(
            "The whole process to generate data took: {} seconds".format(
                    (datetime.now() - start_time).total_seconds()
                )
            )
        