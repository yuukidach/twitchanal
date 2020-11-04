# Generate Token for API

The whole process is [here](https://dev.twitch.tv/docs/authentication). But since some of our groupmates may still be confused about how to do that. I write down this simplified process.

## 1. Register App

Go to this [site](https://dev.twitch.tv/console/apps/create).

![](./res/registerapp.png)

Fill in the blanks.

Write `Name` and choose `Category` as you wish. For `OAuth Redirect URLs`, write: `http://localhost.`

## 2. Get Your ID and Secret

After you finish step 1. There will be a `Client ID` and a `Client Secret`. The ID is fixed and visable. If you can not see your secret, click `New Secret` button to create a new one.

## 3. Get Token

Basic instruction:

``` shell
POST https://id.twitch.tv/oauth2/token
    ?client_id=<your client ID>
    &client_secret=<your client secret>
    &grant_type=client_credentials
    &scope=<space-separated list of scopes> 
```

We can use command line or postman (**recommended**) to do this.

There is the example

### Option 1 - Command line

``` Shell
POST https://id.twitch.tv/oauth2/token?client_id=uo6dggojyb8d6soh92zknwmi5ej1q2&client_secret=nyo51xcdrerl8z9m56w9w6wg&grant_type=client_credentials
```

### Option 2 - Postman

Also, we can use postman to do this:

![](./res/postman.png)

- Choose `POST` and fill the blank with `https://id.twitch.tv/oauth2/token` in header bar.
- Write Params. `client_id` and `client_secret` are what you just got. `grant_type` must be `client_credentials`.

Click `Send` button. BOOM!!! You get your token. and you can do whatever you want now.

## 4. Test Token

Now we have token, but we still need to test if it is available. Test is a very important task in engineering. There is a simple test for you:

``` shell
curl --location --request
GET 'https://api.twitch.tv/helix/search/channels?query=a_seagull' \
--header 'client-id: wbmytr93xzw8zbg0p1izqyzzc5mbiz' \
--header 'Authorization: Bearer 2gbdx6oar67tqtcmt49t3wpcgycthx'
```

Remember to change the id and the token to yours. The code after `Bearer` is the token.

You can also use postman to do this test.
