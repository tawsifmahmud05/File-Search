package com.example.androidproject.Api.verifyUser;

import com.example.androidproject.model.User;
import com.google.gson.annotations.Expose;
import com.google.gson.annotations.SerializedName;

public class VerifyUser {

    @SerializedName("message")
    @Expose
    String message ;

    @SerializedName("error")
    @Expose
    boolean error;

    @SerializedName("data")
    @Expose
    User user;

    public String getMessage() {
        return message;
    }

    public boolean isError() {
        return error;
    }

    public User getUser() {
        return user;
    }
}
