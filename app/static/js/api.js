async function request(url,method="GET",data=None) {
    const options = {
        method,
        headers: {
            "Content-Type":"application/json"
        }
    }

    if (data) {
        options.body=JSON.stringify(data)
    }

    const res = await fetch(url,options)
    return await res.json()


    
}