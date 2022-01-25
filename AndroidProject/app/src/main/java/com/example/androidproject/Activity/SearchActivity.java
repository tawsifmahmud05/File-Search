package com.example.androidproject.Activity;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.appcompat.app.AppCompatActivity;
import androidx.recyclerview.widget.LinearLayoutManager;
import androidx.recyclerview.widget.RecyclerView;

import android.content.Intent;
import android.os.Bundle;
import android.speech.RecognizerIntent;
import android.util.Log;
import android.view.View;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ImageView;
import android.widget.Spinner;
import android.widget.TextView;
import android.widget.Toast;

import com.example.androidproject.Adapter.searchRecyclerviewAdapter;
import com.example.androidproject.Api.SearchList.searchListApi;
import com.example.androidproject.Api.clusterList.clusterListApi;
import com.example.androidproject.Api.verifyUser.VerifyUserApi;
import com.example.androidproject.R;
import com.example.androidproject.RetrofitClass;
import com.example.androidproject.model.Cluster;
import com.example.androidproject.model.SearchModel;
import com.example.androidproject.model.User;
import com.google.android.gms.auth.api.Auth;
import com.google.android.gms.auth.api.signin.GoogleSignInAccount;
import com.google.android.gms.auth.api.signin.GoogleSignInOptions;
import com.google.android.gms.auth.api.signin.GoogleSignInResult;
import com.google.android.gms.common.ConnectionResult;
import com.google.android.gms.common.api.GoogleApiClient;
import com.google.android.gms.common.api.OptionalPendingResult;
import com.google.android.gms.common.api.ResultCallback;
import com.google.android.gms.common.api.Status;

import java.util.ArrayList;
import java.util.List;
import java.util.Locale;
import java.util.Objects;

import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;

public class SearchActivity extends AppCompatActivity implements GoogleApiClient.OnConnectionFailedListener{
    private static final int REQUEST_CODE_SPEECH_INPUT = 1;

    private GoogleApiClient googleApiClient;
    private GoogleSignInOptions gso;

    private Cluster selectedCluster;

    Button logoutBtn,searchbtn;
    private ImageView micButton;
    private TextView usermail;
    private EditText searchKeyword;
    private Spinner searchCluster;

    private RecyclerView recyclerView;

    private User loginuser = new User();

    //        Cluster initialization
    private ArrayList<Cluster> items = new ArrayList<>();
    private ArrayList<SearchModel> searchitems = new ArrayList<>();

    private searchRecyclerviewAdapter searchrecyclerviewadapter;

    private ArrayAdapter<Cluster> adapter;

//    private String mail = "tawsifmahmud05@gmail.com";
    private String token = "Token e697bea2c349db8c61a55accf6c0546db5de0dd8";
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_search);

        micButton = findViewById(R.id.mic);
        searchKeyword = findViewById(R.id.search_keyword);
        searchCluster = findViewById(R.id.search_cluster);
        logoutBtn = (Button) findViewById(R.id.logoutBtn);
        searchbtn = findViewById(R.id.searchBtn);
        usermail = findViewById(R.id.search_email);
        recyclerView = findViewById(R.id.recyclerListView);
        recyclerView.setHasFixedSize(true);
        recyclerView.setLayoutManager(new LinearLayoutManager(this));
        searchrecyclerviewadapter = new searchRecyclerviewAdapter(getApplicationContext(),searchitems);
        recyclerView.setAdapter(searchrecyclerviewadapter);

        gso = new GoogleSignInOptions.Builder(GoogleSignInOptions.DEFAULT_SIGN_IN)
                .requestEmail()
                .build();

        googleApiClient = new GoogleApiClient.Builder(this)
                .enableAutoManage(this, this)
                .addApi(Auth.GOOGLE_SIGN_IN_API, gso)
                .build();


        searchCluster.setOnItemSelectedListener(new AdapterView.OnItemSelectedListener() {
            @Override
            public void onItemSelected(AdapterView<?> adapterView, View view, int i, long l) {
                selectedCluster = (Cluster) adapterView.getSelectedItem();
            }

            @Override
            public void onNothingSelected(AdapterView<?> adapterView) {
                selectedCluster = items.get(0);
            }
        });


//        setRecyclerview();

        searchbtn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {

                searchfiles();
//                    setRecyclerview();



//                searchrecyclerviewadapter = new searchRecyclerviewAdapter(getApplicationContext(),searchitems);
//                recyclerView.setAdapter(searchrecyclerviewadapter);
//                searchrecyclerviewadapter.notifyDataSetChanged();
//                recyclerView.setAdapter(searchrecyclerviewadapter);
            }
        });

        logoutBtn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Auth.GoogleSignInApi.signOut(googleApiClient).setResultCallback(
                        new ResultCallback<Status>() {
                            @Override
                            public void onResult(Status status) {
                                if (status.isSuccess()) {
                                    gotoMainActivity();
                                } else {
                                    Toast.makeText(getApplicationContext(), "Session not close", Toast.LENGTH_LONG).show();
                                }

                            }


                        });
            }
        });

//        Speech to Text
        micButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {

                Intent intent = new Intent(RecognizerIntent.ACTION_RECOGNIZE_SPEECH);
                intent.putExtra(RecognizerIntent.EXTRA_LANGUAGE_MODEL, RecognizerIntent.LANGUAGE_MODEL_FREE_FORM);
                intent.putExtra(RecognizerIntent.EXTRA_LANGUAGE, Locale.getDefault());
                intent.putExtra(RecognizerIntent.EXTRA_PROMPT, "Speak to text");
                micButton.setBackground(getDrawable(R.drawable.ic_voice_red));
                try {
                    startActivityForResult(intent, REQUEST_CODE_SPEECH_INPUT);
                } catch (Exception e) {
                    Toast.makeText(SearchActivity.this, " " + e.getMessage(), Toast.LENGTH_SHORT).show();
                    micButton.setBackground(getDrawable(R.drawable.ic_voice));

                }
            }
        });
    }

    private void setRecyclerview() {
            searchrecyclerviewadapter = new searchRecyclerviewAdapter(getApplicationContext(),searchitems);
            recyclerView.setAdapter(searchrecyclerviewadapter);



    }

    private void searchfiles() {

        searchitems.clear();

        // INITIALIZE RETROFIT
        RetrofitClass retrofitClass = new RetrofitClass();
        searchListApi searchListApi = retrofitClass.getRetrofit().create(searchListApi.class);

        String keyword = searchKeyword.getText().toString();
        String clusderid = String.valueOf(selectedCluster.getId());


        //CALL THE REQUEST
        Call<List<SearchModel>> call = searchListApi.getSearchList(keyword,clusderid);


        call.enqueue(new Callback<List<SearchModel>>() {
            @Override
            public void onResponse(Call<List<SearchModel>> call, Response<List<SearchModel>> response) {

                if(response.isSuccessful()){
                    Toast.makeText(getApplicationContext(),"successful",Toast.LENGTH_LONG).show();
                    List<SearchModel> searchresult =response.body();


                    for(SearchModel model : searchresult){
                        try{
                            searchitems.add(model);
                            Toast.makeText(getApplicationContext(),model.getId(),Toast.LENGTH_LONG).show();
                        }catch(Exception e){

                        }

                    }
                    for(SearchModel model : searchitems){
                        model.setKeyword(keyword);
                    }
                    searchrecyclerviewadapter.notifyDataSetChanged();
                }

            }

            @Override
            public void onFailure(Call<List<SearchModel>> call, Throwable t) {
                Log.d("verify",t.getMessage());
                Toast.makeText(getApplicationContext(),t.getMessage(),Toast.LENGTH_LONG).show();

            }
        });
    }

    @Override
    protected void onStart() {

        super.onStart();
        OptionalPendingResult<GoogleSignInResult> opr= Auth.GoogleSignInApi.silentSignIn(googleApiClient);
        if(opr.isDone()){
            GoogleSignInResult result=opr.get();
            handleSignInResult(result);
        }else{
            opr.setResultCallback(new ResultCallback<GoogleSignInResult>() {
                @Override
                public void onResult(@NonNull GoogleSignInResult googleSignInResult) {
                    handleSignInResult(googleSignInResult);
                }
            });
        }
    }

    private void handleSignInResult(GoogleSignInResult result){
        if(result.isSuccess()){
            GoogleSignInAccount account=result.getSignInAccount();
//            userName.setText(account.getDisplayName());
//            userEmail.setText(account.getEmail());
//            userId.setText(account.getId());
//            usermail.setText(account.getDisplayName());
            checkuser(account.getEmail());


//            checkuser(account.getEmail());

//            try{
//                Glide.with(this).load(account.getPhotoUrl()).into(profileImage);
//            }catch (NullPointerException e){
//                Toast.makeText(getApplicationContext(),"image not found",Toast.LENGTH_LONG).show();
//            }

        }else{
            gotoMainActivity();
        }
    }

    private void getcluster(int id) {
        items.clear();

        // INITIALIZE RETROFIT
        RetrofitClass retrofitClass = new RetrofitClass();
        clusterListApi clusterListApi = retrofitClass.getRetrofit().create(clusterListApi.class);


        //CALL THE REQUEST
        Call<List<Cluster>> call = clusterListApi.getClusterList(id);


        call.enqueue(new Callback<List<Cluster>>() {
            @Override
            public void onResponse(Call<List<Cluster>> call, Response<List<Cluster>> response) {

                if(response.isSuccessful()){
                    Toast.makeText(getApplicationContext(),"successful",Toast.LENGTH_LONG).show();
                    List<Cluster> clusters =response.body();

                    for(Cluster cluster : clusters){
                        try{
                            items.add(cluster);
                            adapter = new ArrayAdapter<Cluster>(getApplicationContext(),
                                     android.R.layout.simple_spinner_dropdown_item,
                                     items);
                            searchCluster.setAdapter(adapter);
                        }catch(Exception e){

                        }

                    }
                }

            }

            @Override
            public void onFailure(Call<List<Cluster>> call, Throwable t) {
                Log.d("verify",t.getMessage());
                Toast.makeText(getApplicationContext(),t.getMessage(),Toast.LENGTH_LONG).show();

            }
        });

    }

    private void checkuser(String email) {

        // INITIALIZE RETROFIT
        RetrofitClass retrofitClass = new RetrofitClass();
        VerifyUserApi verifyUserApi = retrofitClass.getRetrofit().create(VerifyUserApi.class);


        //CALL THE REQUEST
        Call<List<User>> call = verifyUserApi.getUser(email);//"Token "+ token


        call.enqueue(new Callback<List<User>>() {
            @Override
            public void onResponse(Call<List<User>> call, Response<List<User>> response) {

                if(response.isSuccessful()){

                    List<User> users =response.body();
                    if(users.isEmpty()){
                        searchbtn.setVisibility(View.GONE);
                        usermail.setText("SignIn from web\nAnd Create Cluster to search");
                        Toast.makeText(getApplicationContext(),"No user with this email",Toast.LENGTH_LONG).show();

                    }else{
                        Toast.makeText(getApplicationContext(),"successful",Toast.LENGTH_LONG).show();
                        for(User user : users){
                            loginuser = user;
                            String responsetest = "";
                            usermail.setText(user.getEmail());
                            getcluster(user.getId());
                            responsetest += user.getEmail();
                            Log.v("Tag",""+responsetest);
                            break;
                        }
                    }


                }

            }

            @Override
            public void onFailure(Call<List<User>> call, Throwable t) {
                Log.d("verify",t.getMessage());
                Toast.makeText(getApplicationContext(),t.getMessage(),Toast.LENGTH_LONG).show();

            }
        });
    }

    @Override
    protected void onActivityResult(int requestCode, int resultCode, @Nullable Intent data)
    {
        micButton.setBackground(getDrawable(R.drawable.ic_voice));
        super.onActivityResult(requestCode, resultCode, data);
        if (requestCode == REQUEST_CODE_SPEECH_INPUT) {
            if (resultCode == RESULT_OK && data != null) {
                ArrayList<String> result = data.getStringArrayListExtra(RecognizerIntent.EXTRA_RESULTS);
                searchKeyword.setText(Objects.requireNonNull(result).get(0));

            }
        }
    }

    private void gotoMainActivity(){
        Intent intent=new Intent(this, LoginScreenActivity.class);
        startActivity(intent);
    }





    @Override
    public void onConnectionFailed(@NonNull ConnectionResult connectionResult) {

    }
}