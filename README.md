# Shinshin

Test project for `apimodel` working with [enka.network](https://enka.shinshin.moe/)

Won't release on pypi.

```py
import shinshin

client = shinshin.Client()

user = await client.get_user(710785423)
```