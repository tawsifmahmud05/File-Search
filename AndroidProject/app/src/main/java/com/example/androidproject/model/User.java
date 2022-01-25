package com.example.androidproject.model;

import com.google.gson.annotations.Expose;
import com.google.gson.annotations.SerializedName;

public class User {

    @SerializedName("id")
    @Expose
    private int id;

    @SerializedName("username")
    @Expose
    private String username;


    @SerializedName("email")
    @Expose
    private String email;

    public int getId() {
        return id;
    }



    public String getUsername() {
        return username;
    }


    public String getEmail() {
        return email;
    }




}
