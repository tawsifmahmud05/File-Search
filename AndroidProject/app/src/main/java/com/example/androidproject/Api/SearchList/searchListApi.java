package com.example.androidproject.Api.SearchList;

import com.example.androidproject.model.SearchModel;

import java.util.List;

import retrofit2.Call;
import retrofit2.http.GET;
import retrofit2.http.Query;

public interface searchListApi {

    @GET("file")
    Call<List<SearchModel>> getSearchList (@Query("search") String keyword, @Query("filecluster") String id);//@Header("Authorization") String token
}
