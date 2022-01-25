package com.example.androidproject.model;

import com.google.gson.annotations.Expose;
import com.google.gson.annotations.SerializedName;

public class Cluster {
    @SerializedName("id")
    @Expose
    private int id;

    @SerializedName("name")
    @Expose
    private String name;

    @SerializedName("crawled")
    @Expose
    private boolean crawled;

    @SerializedName("owner")
    @Expose
    private int owner;

    public int getId() {
        return id;
    }

    public String getName() {
        return name;
    }

    public boolean isCrawled() {
        return crawled;
    }

    public int getOwner() {
        return owner;
    }

    @Override
    public String toString() {
        return name;
    }
}
