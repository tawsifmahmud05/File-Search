package com.example.androidproject.Api.clusterList;

import com.example.androidproject.model.Cluster;

import java.util.List;

import retrofit2.Call;
import retrofit2.http.GET;
import retrofit2.http.Query;

public interface clusterListApi {

    @GET("clusterlist")
    Call<List<Cluster>> getClusterList (@Query("owner") int owner);//@Header("Authorization") String token


}
