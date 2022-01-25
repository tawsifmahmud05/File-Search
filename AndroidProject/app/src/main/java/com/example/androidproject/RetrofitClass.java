package com.example.androidproject;

import okhttp3.OkHttpClient;
import retrofit2.Retrofit;
import retrofit2.converter.gson.GsonConverterFactory;

public class RetrofitClass {

    public Retrofit getRetrofit(){

//        String url = "http://192.168.0.105:8000/api/"; //172.20.80.1
        String url = "http://10.0.2.2:8000/api/"; //172.20.80.1


        // RETROFIT
        OkHttpClient.Builder httpClient = new OkHttpClient.Builder();
        Retrofit retrofit = new Retrofit.Builder()
                .baseUrl(url)
                .addConverterFactory(GsonConverterFactory.create())
                .client(httpClient.build())
                .build();

        return retrofit;

    }
}
