package org.renpy.android;

import android.app.Activity;
import android.os.Bundle;

import android.widget.TextView;
import org.renpy.android.R;

public class GetTextActivity extends Activity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_get_text);
        setOutputText("numbers here...");

        GetText mGT = new GetText();
        String out = mGT.getText(this,"alpha_w4");
        setOutputText(out);
    }



    public void setOutputText(String text) {
        TextView mOut = (TextView)findViewById(R.id.outputtext);
        mOut.setText(text);
    }
}
