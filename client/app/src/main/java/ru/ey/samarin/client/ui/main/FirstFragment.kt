package ru.ey.samarin.client.ui.main

import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import androidx.fragment.app.Fragment
import ru.ey.samarin.client.R
import ru.ey.samarin.client.databinding.FragmentFirstBinding

/**
 * A simple [Fragment] subclass as the default destination in the navigation.
 */
class FirstFragment : Fragment() {

    companion object {
        const val ARG_LOGIN_RESULT = "ARG_LOGIN_RESULT"
    }

    private var _binding: FragmentFirstBinding? = null

    // This property is only valid between onCreateView and
    // onDestroyView.
    private val binding get() = _binding!!

    private val loginResult by lazy {
        requireActivity().intent.getStringExtra(ARG_LOGIN_RESULT)
    }

    override fun onCreateView(
        inflater: LayoutInflater, container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View {
        _binding = FragmentFirstBinding.inflate(inflater, container, false)
        return binding.root
    }

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)

        val welcomeText = "${getString(R.string.welcome)} $loginResult"
        binding.textviewFirst.text = welcomeText
    }

    override fun onDestroyView() {
        super.onDestroyView()
        _binding = null
    }
}