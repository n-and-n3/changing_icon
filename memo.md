## get users/me

response example
```
{
  "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
  "bio": "string",
  "groups": [
    "3fa85f64-5717-4562-b3fc-2c963f66afa6"
  ],
  "tags": [
    {
      "tagId": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
      "tag": "string",
      "isLocked": true,
      "createdAt": "2026-03-31T15:45:39.882Z",
      "updatedAt": "2026-03-31T15:45:39.882Z"
    }
  ],
  "updatedAt": "2026-03-31T15:45:39.882Z",
  "lastOnline": "2026-03-31T15:45:39.882Z",
  "twitterId": "rypDY",
  "name": "-mB4h6CkRAYozAlyWGwvl5pMn",
  "displayName": "string",
  "iconFileId": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
  "bot": true,
  "state": 0,
  "permissions": [
    "get_webhook"
  ],
  "homeChannel": "3fa85f64-5717-4562-b3fc-2c963f66afa6"
}
```

## patch users/me

request exsample
```
{
  "displayName": "string",
  "twitterId": "JcUtb",
  "bio": "string",
  "homeChannel": "3fa85f64-5717-4562-b3fc-2c963f66afa6"
}
```