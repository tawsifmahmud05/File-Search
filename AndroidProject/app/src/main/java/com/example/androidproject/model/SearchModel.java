package com.example.androidproject.model;

import com.google.gson.annotations.Expose;
import com.google.gson.annotations.SerializedName;

public class SearchModel {

    @SerializedName("id")
    @Expose
    private int id;

    @SerializedName("mainurl")
    @Expose
    private String mainurl;

    @SerializedName("fileurl")
    @Expose
    private String fileurl;

    @SerializedName("content")
    @Expose
    private String content;

    @SerializedName("filecluster")
    @Expose
    private String filecluster;

    private String keyword;

    public String getKeyword() {
        return keyword;
    }

    public void setKeyword(String keyword) {
        this.keyword = keyword;
    }

    public int getId() {
        return id;
    }

    public String getMainurl() {
        return mainurl;
    }

    public String getFileurl() {
        return fileurl;
    }

    public String getContent() {
        return content;
    }

    public String getFilecluster() {
        return filecluster;
    }
}
