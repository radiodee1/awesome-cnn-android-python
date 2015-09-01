package org.renpy.android;

import android.app.Activity;
//import android.app.Application;
import android.content.Context;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
//import java.lang.reflect.Field;
//import java.util.ArrayList;
import org.renpy.android.ResourceManager;


public class GetText {

    Context context;

    public ResourceManager mManager;

    public void GetText() {


    }


    public String getText(Activity c, String in) {

        mManager = new ResourceManager(c);
        int mId = mManager.getIdentifier(in,"raw");

        context = c.getApplicationContext();

        String out = "";

        if (true) {

            InputStream inputStream = context.getResources().openRawResource(mId);

            InputStreamReader inputreader = new InputStreamReader(inputStream);
            BufferedReader buffreader = new BufferedReader(inputreader);
            String line;
            StringBuilder text = new StringBuilder();

            try {
                while ((line = buffreader.readLine()) != null) {
                    text.append(line);
                    text.append('\n');
                }
            } catch (IOException e) {
                return null;
            }

            try {
                //return text.toString();
                byte[] convert = text.toString().getBytes("UTF-8");
                out = new String (convert, "UTF-8");
            }
            catch (Exception e) {e.printStackTrace();}

        }
        return out;
    }
}
