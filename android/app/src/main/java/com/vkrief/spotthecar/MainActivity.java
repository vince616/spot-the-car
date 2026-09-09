package com.vkrief.spotthecar;

import android.os.Bundle;
import com.getcapacitor.BridgeActivity;

public class MainActivity extends BridgeActivity {
    @Override
    public void onCreate(Bundle savedInstanceState) {
        registerPlugin(TcfPlugin.class);
        super.onCreate(savedInstanceState);
    }
}
