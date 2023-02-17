package ru.ey.samarin.client.di

import dagger.Module
import dagger.Provides
import dagger.hilt.InstallIn
import dagger.hilt.components.SingletonComponent
import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory
import ru.ey.samarin.client.data.LoginApi
import ru.ey.samarin.client.data.LoginDataSource
import javax.inject.Singleton

@Module
@InstallIn(SingletonComponent::class)
object AppModule {

    @Provides
    fun providesBaseUrl() : String = "https://example-hilt-retrofit-default-rtdb.firebaseio.com/"

    @Provides
    @Singleton
    fun provideRetrofit(BASE_URL : String) : Retrofit = Retrofit.Builder()
        .addConverterFactory(GsonConverterFactory.create())
        .baseUrl(BASE_URL)
        .build()

    @Provides
    @Singleton
    fun provideLoginApi(retrofit : Retrofit) : LoginApi = retrofit.create(LoginApi::class.java)

    @Provides
    @Singleton
    fun provideMainRemoteData(loginApi : LoginApi) : LoginDataSource = LoginDataSource(loginApi)
}