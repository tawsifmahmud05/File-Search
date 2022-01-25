package com.example.androidproject.Adapter;

import android.content.Context;
import android.text.method.LinkMovementMethod;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.TextView;

import androidx.annotation.NonNull;
import androidx.recyclerview.widget.RecyclerView;

import com.example.androidproject.R;
import com.example.androidproject.model.SearchModel;

import java.util.ArrayList;
import java.util.List;

public class searchRecyclerviewAdapter extends RecyclerView.Adapter<searchRecyclerviewAdapter.Viewholder>{

    private Context context;
    private List<SearchModel> searchList;

    // Constructor
    public searchRecyclerviewAdapter(Context context, List<SearchModel> searchList) {
        this.context = context;
        this.searchList = searchList;
    }

    @NonNull
    @Override
    public searchRecyclerviewAdapter.Viewholder onCreateViewHolder(@NonNull ViewGroup parent, int viewType) {

        LayoutInflater layoutInflater = LayoutInflater.from(parent.getContext());
        View view = layoutInflater.inflate(R.layout.recyclerview_searchresult,parent,false);
        return new Viewholder(view);
    }

    @Override
    public void onBindViewHolder(@NonNull searchRecyclerviewAdapter.Viewholder holder, int position) {
        SearchModel model = searchList.get(position);
        holder.keyword.setText(""+model.getKeyword());
        String text = abbreviate(model.getContent().trim(), 40);
        holder.content.setText(""+text);
        holder.link.setText(""+model.getFileurl());


    }

    @Override
    public int getItemCount() {
        return searchList.size();
    }

    public class Viewholder extends RecyclerView.ViewHolder {

        TextView keyword,content,link;
        public Viewholder(@NonNull View itemView) {
            super(itemView);
            keyword = itemView.findViewById(R.id.card_key);
            content = itemView.findViewById(R.id.card_desc);
            link = itemView.findViewById(R.id.card_link);
            link.setMovementMethod(LinkMovementMethod.getInstance());
        }
    }

//    public void changeDataset(ArrayList<SearchModel> yourList) {
//        searchList = yourList ;
//        notifyDataSetChanged();
//
//    }

    public static String abbreviate(String text,int maxFront){
        if(text.length() > maxFront){
            text = text.substring(0,maxFront)+"...";
        }
        return text;
    }

}
