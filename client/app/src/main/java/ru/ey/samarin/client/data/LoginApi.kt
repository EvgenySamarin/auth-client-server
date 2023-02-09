package ru.ey.samarin.client.data

import retrofit2.Response
import retrofit2.http.GET
import retrofit2.http.Path

interface LoginApi {

    @GET("User/{userId}.json")
    suspend fun getUser(@Path("userId") userId : Int) : Response<Any>
}