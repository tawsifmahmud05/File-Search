package com.example.androidproject.Api.verifyUser;

import com.example.androidproject.model.User;
import com.google.gson.annotations.Expose;
import com.google.gson.annotations.SerializedName;

import java.util.List;

import retrofit2.Call;
import retrofit2.http.GET;
import retrofit2.http.Header;
import retrofit2.http.Query;

public interface VerifyUserApi {

    @GET("users")
    Call<List<User>> getUser (@Query ("email") String email);//@Header("Authorization") String token
}
